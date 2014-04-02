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

from mro_contact.models import Department, Employee
from mro_warehouse.models import Item, Warehouse, WarehouseItem

#from mro_system_type.models import SystemType

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

class Equipment(models.Model):
    '''
    
    '''
    # the system identification
    name = models.CharField(_('Equipment Name'), max_length = 30)
    serial_number = models.CharField(_('Serial number'), max_length = 30, blank = True, null = True)
    
    system = models.ForeignKey('System')
    system.verbose_name = _('System Maintenance Card')
    
    # system location
    location = models.CharField(_('Location'), max_length = 30, blank = True, null = True)
    sublocation = models.CharField(_('Secondary Location'), max_length = 30, blank = True, null = True)

    assign_to = models.ForeignKey(Employee, null = True, blank = True)
    assign_to.verbose_name = _('Maintenance employee')

#    contract_number = models.CharField(_('Contract number'), max_length = 30, null = True, blank = True)
#    contract_include_parts = models.BooleanField(_('Contract include parts'), help_text = _('Check this box if the contract include parts'))

    # what department if responsible for this system
    department = models.ForeignKey(Department)
    department.verbose_name = _('Equipment\'s Department')
    
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
    image.verbose_name = _('Equipment Image')
    
    # more information about this equpment
    description = models.CharField(_('Equipment\'s Description'), max_length = 255, null = True, blank = True)
    
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
    
    counter_command = models.CharField(_('Counter Command'), max_length = 60, null = True, blank = True)
    counter_reset_command = models.CharField(_('Counter Reset Command'), max_length = 60, null = True, blank = True)
    
    counter_protocol = models.CharField(_('Counter Protocol'), 
                                            max_length = 60, 
                                            null = True, 
                                            blank = True, 
                                            choices=[('tcp','TCP'),
                                                     ('tal','Serial over TCP')])

    counter_ip = models.CharField(_('Counter IP Address'), max_length = 60, null = True, blank = True)
    
    cpus = [(str(i+1),str(i+1)) for i in xrange(31)]
    counter_cpu = models.CharField(_('Counter CPU'), max_length = 60, null = True, blank = True, choices=cpus)
    counter_com = models.CharField(_('Counter COM'), max_length = 2, null = True, blank = True)

    counter_parameter = models.CharField(_('Counter Parameter'), max_length = 60, null = True, blank = True)
    counter_file = models.IntegerField(_('Counter File'), null = True, blank = True)
    counter_reset_parameter = models.CharField(_('Counter Reset Parameter'), max_length = 60, null = True, blank = True)
    
    counter_reset_file = models.IntegerField(_('Counter Reset File'), null = True, blank = True)
    
    current_counter_value = models.IntegerField(_('Current Value'), null = True, blank = True)
    
    def has_hourly_maintenance(self):
        return self.system.has_hourly_maintenance()
        
    def has_daily_maintenance(self):
        return self.system.has_daily_maintenance()
    
    def has_weekly_maintenance(self):
        return self.system.has_weekly_maintenance()
        
    def has_monthly_maintenance(self):
        return self.system.has_monthly_maintenance()
        
    def has_yearly_maintenance(self):
        return self.system.has_yearly_maintenance()
        
    # model overides
    def __unicode__(self):
        if self.name:
          return self.name
        elif self.description:
          short_desc = self.description.split('\n')[0].split()[:8]
          return '%s' % (' '.join(short_desc))
        return 'Equipment'
    
    class Meta:
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipments')
        ordering = ('name',)

class System(models.Model):
    ''' an system site
    
        the system and the system maintainer contact information
    '''
    
    # the system identification
    name = models.CharField(_('System Card Name'), max_length = 30)
    serial_number = models.CharField(_('Serial number'), max_length = 30, blank = True, null = True)
    
    # what department if responsible for this system
    department = models.ForeignKey(Department, blank=True, null=True)
    department.verbose_name = _('System Department')
    
    # more information about this equpment
    description = models.CharField(_('System Description'), max_length = 255, null = True, blank = True)
    
    # documents for this job
    documents = models.ManyToManyField('SystemDocument', 
                                       related_name = 'system_documents', 
                                       null = True, 
                                       blank = True)
    documents.verbose_name = _('Documents')
    
#    system_types = models.ManyToManyField(SystemType, 
#                                          related_name = 'system_type', 
#                                          null = True, 
#                                          blank = True)
#    system_types.verbose_name = _('System Type')
    
#    def system_types_list(self):
#      '''
#      '''
#      return ','.join([st.name for st in self.system_types.all()])

    def has_hourly_maintenance(self):
        ''' True if the system has an hourly maintenance
        '''
        
        hourly_maintenances = Maintenance.objects.filter(system = self, work_type = 'WH')
        return len(hourly_maintenances) > 0
    has_hourly_maintenance.verbose_name = _('Hourly')

    def has_daily_maintenance(self):
        ''' True if the system has an Daily maintenance
        '''
        
        daily_maintenances = Maintenance.objects.filter(system = self, work_type = 'DA')
        return len(daily_maintenances) > 0
    has_daily_maintenance.short_description = _('Daily')

    def has_weekly_maintenance(self):
        ''' True if the system has an weekly maintenance
        '''
        
        weekly_maintenances = Maintenance.objects.filter(system = self, work_type = 'WE')
        return len(weekly_maintenances) > 0
    has_weekly_maintenance.short_description = _('Weekly')

    def has_monthly_maintenance(self):
        ''' True if the system has an monthly maintenance
        '''
        
        monthly_maintenances = Maintenance.objects.filter(system = self, work_type = 'MO')
        return len(monthly_maintenances) > 0
    has_monthly_maintenance.short_description = _('Monthly')

    def has_yearly_maintenance(self):
        ''' True if the system has an yearly maintenance
        '''
        
        monthly_maintenances = Maintenance.objects.filter(system = self, work_type = 'YE')
        return len(monthly_maintenances) > 0
    has_yearly_maintenance.short_description = _('Yearly')

    # model overides
    def __unicode__(self):
        if self.name:
          return self.name
        elif self.description:
          short_desc = self.description.split('\n')[0].split()[:8]
          return '%s' % (' '.join(short_desc))
        return 'System'
    
    class Meta:
        verbose_name = _('System Maintenance Card')
        verbose_name_plural = _('System Maintenance Cards')
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
    
    WORK_TYPE = (
        ('WH', _('Hourly')),
        ('DA', _('Daily')),
        ('WE', _('Weekly')),
        ('MO', _('Monthly')),
        ('YE', _('Yearly')),
        ('ON', _('One time')),
    )

    # this work is on this system
    system = models.ForeignKey(System)
    system.verbose_name = _('System')
    
    # is this a priority job
    priority = models.ForeignKey(Priority, related_name = 'maintenance_priority', null = True, blank = True)
    priority.verbose_name = _('Priority')
    
    work_type = models.CharField(max_length = 2, choices = WORK_TYPE, default = 'WH')
    work_type.verbose_name = _('Maintenance type')

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
#    last_maintenance = models.DateField(null = True, blank = True)
#    last_maintenance.verbose_name = _('Last Maintenance Date')
    
    # command to read work hours
    counter_command = models.CharField(_('Counter Command'), max_length = 60, null = True, blank = True)
#    current_counter_value = models.FloatField(_('Current Counter Value'), default = 0.0, null = True, blank = True)
#    last_maintenance_counter_value = models.FloatField(_('Last Maintenance Counter Value'), default = 0.0, null = True, blank = True)

    def work_cycle_str(self):
        ''' human readable text representing a work cycle
        '''
        cycle_as_string = "%d" % self.work_cycle_count

        # print out the work cycle and work_count
        if self.work_cycle_count == 1:
            cycle_as_string = _('%(cycle)s') % {'cycle': self.get_work_type_display() }
        else:
            cycle_as_string = _('%(count)d %(cycle)s') % {'count': self.work_cycle_count, 'cycle': self.get_work_cycle_display() }
        
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
        
        # make work cycle compatible with the work type
        #if self.work_type == 'WH' and self.work_cycle != 'WH':
        #    self.work_type = self.work_cycle

        #if self.work_type != 'WH' and self.work_cycle == 'WH':
        #    self.work_type = self.work_cycle
        self.work_type = self.work_cycle
        
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

class SystemDocument(models.Model):
    ''' Documents used for the Order
    '''
    # connection
    system = models.ForeignKey(System)
    system.verbose_name = _('System')

    # description
    title = models.CharField(_('Document title'), max_length = 30)
    description =  models.TextField(_('Document description'), blank = True, null = True)
    created = models.DateField(default=lambda: date.today())
    created.verbose_name = _('Created date')
    
    # the document
    image = models.FileField(null=True, blank=True, upload_to='documents/%Y/%m/%d')
    image.verbose_name = _('Document')

    class Meta:
        verbose_name = _('System Document')
        verbose_name_plural = _('System Documents')
        ordering = ('title',)
        
