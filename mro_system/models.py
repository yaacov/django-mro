#!/usr/bin/env python
# -*- coding:utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2013 Yaacov Zamir <kobi.zamir@gmail.com>
# Author: Yaacov Zamir (2013) <kobi.zamir@gmail.com>

from datetime import date, datetime, timedelta

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from mro_contact.models import Department, Employee, Suplier
from mro_warehouse.models import Item, Warehouse, WarehouseItem

class Priority(models.Model):
    ''' work/system priority
        
        is this a priority job ?
        how many days we can leave it un-done.
    '''
    
    # the priority identification string
    name = models.CharField(_('Priority'), max_length = 30)
    
    # number of days we can leave the job un-done
    max_days_delay = models.IntegerField(_('Max delay in days'), default = 2)
    
    # model overides
    def __unicode__(self):
        return '%s' % (self.name)
    
    class Meta:
        verbose_name = _('Priority')
        verbose_name_plural = _('Priority')
        ordering = ('max_days_delay',)

class System(models.Model):
    ''' an system site
    
        the system and the system maintainer contact information
    '''
    
    # the system identification
    name = models.CharField(_('System Name'), max_length = 30)
    serial_number = models.CharField(_('Serial number'), max_length = 30, blank = True, null = True)
    
    suplier = models.ForeignKey(Suplier, null = True, blank = True)
    suplier.verbose_name = _('System Suplier')

    assign_to = models.ForeignKey(Employee, null = True, blank = True)
    assign_to.verbose_name = _('Maintenance employee')

    card_number = models.CharField(_('Card number'), max_length = 30, null = True, blank = True)

    contract_number = models.CharField(_('Contract number'), max_length = 30, null = True, blank = True)
    contract_include_parts = models.BooleanField(_('Contract include parts'), help_text = _('Check this box if the contract include parts'))

    # what department if responsible for this system
    department = models.ForeignKey(Department)
    department.verbose_name = _('System Department')
    
    # contact information
    phone = models.CharField(_('Phone'), 
        max_length = 30, blank = True, null = True)
    cell_phone = models.CharField(_('Cell Phone'), 
        max_length = 30, blank = True, null = True)
    address = models.CharField(_('Address'), 
        max_length = 30, blank = True, null = True)
    email = models.EmailField(_('Email'), 
        max_length = 30, blank = True, null = True)
    
    # image - profile image or profile icon
    image = models.ImageField(null=True, blank=True, upload_to='system/')
    image.verbose_name = _('System Image')
    
    # more information about this equpment
    description = models.TextField(_('System Description'))
    
    # install date
    installed = models.DateField(default=lambda: date.today())
    installed.verbose_name = _('Installed')
    
    # we do not delete system from the data base,
    # but if this equpment is not active, we do not show
    # it on tables and reports
    is_active = models.BooleanField('Active', default = True)
    
    # last completed maintenance round
    # for show only, we can not calculate next maintenance becouse
    # we do not have a maintenance cycle for system
    # it is the responsibilty of the maintenanace model to update this form
    last_maintenance = models.DateField(null = True, blank = True)
    last_maintenance.verbose_name = _('Last Maintenance Date')

    # model overides
    def __unicode__(self):
        short_desc = self.description.split('\n')[0].split()[:8]
        return '%s' % (' '.join(short_desc))
    
    class Meta:
        verbose_name = _('System')
        verbose_name_plural = _('System')
        ordering = ('name',)

class Maintenance(models.Model):
    ''' maintenance instructions
        
        when and how to do a maintenance job
    '''
    
    WORK_CYCLE = (
        ('WH', _('Work hours')),
        ('DA', _('Days')),
        ('WE', _('Weeks')),
        ('MO', _('Months')),
        ('YE', _('Years')),
        ('ON', _('Once')),
    )
    
    # this work is on this system
    system = models.ForeignKey(System)
    system.verbose_name = _('System')
    
    # is this a priority job
    priority = models.ForeignKey(Priority, default = 1)
    priority.verbose_name = _('Priority')
    
    # the job manager and contact information
    assign_to = models.ForeignKey(Employee, null = True, blank = True)
    assign_to.verbose_name = _('Assign to')
    
    # estimated time to complete the job
    estimated_work_time = models.IntegerField(_('Estimated work hours'), default = 8)
    
    # what to do
    work_description = models.TextField(_('Work description'))
    
    # items needed to complete this job
    items = models.ManyToManyField(Item, related_name = 'maintenance_items', through = 'MaintenanceItem', null = True, blank = True)
    items.verbose_name = _('MaintenanceItem Item')
    
    # when to do the job
    work_cycle_count = models.IntegerField(_('Maintenance done every'), default = 1)
    work_cycle = models.CharField(max_length = 2, choices = WORK_CYCLE, default = 'WH')
    work_cycle.verbose_name = _('Time periods')

    # last completed maintenance round
    # we use this information to calculate next maintenance time
    last_maintenance = models.DateField(null = True, blank = True)
    last_maintenance.verbose_name = _('Last Maintenance Date')
    
    # command to read work hours
    counter_command = models.CharField(_('Counter Command'), max_length = 60, null = True, blank = True)
    current_counter_value = models.FloatField(_('Current Counter Value'), default = 0.0, null = True, blank = True)
    last_maintenance_counter_value = models.FloatField(_('Last Maintenance Counter Value'), default = 0.0, null = True, blank = True)

    def work_cycle_str(self):
        ''' human readable text representing a work cycle
        '''
        cycle_as_string = 'None'
        
        # get work_cycle information
        cycle_type = self.work_cycle
        cycle_count = self.work_cycle_count
        cycle_type_dict = dict(self.WORK_CYCLE)
        
        # print out the work cycle and work_count
        if cycle_count == 1:
            cycle_as_string = _('One %(cycle)s') % {'count': cycle_count, 'cycle': cycle_type_dict[cycle_type]}
        else:
            cycle_as_string = _('%(count)d %(cycle)s') % {'count': cycle_count, 'cycle': cycle_type_dict[cycle_type]}
        
        return cycle_as_string
    work_cycle_str.verbose_name = _('Work cycle')
    
    def save(self, *args, **kwargs):
        try:
            if (self.last_maintenance and 
                    (not self.system.last_maintenance or 
                        self.system.last_maintenance < self.last_maintenance)):
                self.system.last_maintenance = self.last_maintenance
                self.system.save()
        except Exception, e:
            print e
            pass
        
        # call the default save method
        super(Maintenance, self).save(*args, **kwargs)

    # model overides
    def __unicode__(self):
        short_desc = self.work_description.split()[:5]
        
        return '%s' % (' '.join(short_desc))
    
    class Meta:
        verbose_name = _('Maintenance')
        verbose_name_plural = _('Maintenance')
        ordering = ('system',)

class MaintenanceItem(models.Model):
    ''' Items used for the maintenance
    '''
    
    # connection
    maintenance = models.ForeignKey(Maintenance)
    maintenance.verbose_name = _('Maintenance')
    item = models.ForeignKey(Item, related_name = 'maintenance_item')
    item.verbose_name = _('Item')
    
    # amount of items used
    amount = models.IntegerField(_('Amount'), default = 1)
    
    class Meta:
        verbose_name = _('Maintenance Item')
        verbose_name_plural = _('Maintenance Items')
        ordering = ('maintenance',)
