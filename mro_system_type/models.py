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

from mro_contact.models import Department

class SystemType(models.Model):
    name = models.CharField(_('System Type Name'), max_length = 30)
    description = models.CharField(_('System Type Description'), max_length = 255)
    
    department = models.ForeignKey(Department)
    department.verbose_name = _('System Type Department')
    
    def has_hourly_maintenance(self):
        ''' True if the system has an hourly maintenance
        '''
        
        hourly_maintenances = SystemTypeMaintenance.objects.filter(system_type = self, work_type = 'WH')
        return len(hourly_maintenances) > 0
    has_hourly_maintenance.verbose_name = _('Hourly')

    def has_daily_maintenance(self):
        ''' True if the system has an Daily maintenance
        '''
        
        daily_maintenances = SystemTypeMaintenance.objects.filter(system_type = self, work_type = 'DA')
        return len(daily_maintenances) > 0
    has_daily_maintenance.short_description = _('Daily')

    def has_weekly_maintenance(self):
        ''' True if the system has an weekly maintenance
        '''
        
        weekly_maintenances = SystemTypeMaintenance.objects.filter(system_type = self, work_type = 'WE')
        return len(weekly_maintenances) > 0
    has_weekly_maintenance.short_description = _('Weekly')

    def has_monthly_maintenance(self):
        ''' True if the system has an monthly maintenance
        '''
        
        monthly_maintenances = SystemTypeMaintenance.objects.filter(system_type = self, work_type = 'MO')
        return len(monthly_maintenances) > 0
    has_monthly_maintenance.short_description = _('Monthly')

    def has_yearly_maintenance(self):
        ''' True if the system has an yearly maintenance
        '''
        
        monthly_maintenances = SystemTypeMaintenance.objects.filter(system_type = self, work_type = 'YE')
        return len(monthly_maintenances) > 0
    has_yearly_maintenance.short_description = _('Yearly')

    # model overides
    def __unicode__(self):
        short_desc = self.description.split('\n')[0].split()[:8]
        return '%s' % (' '.join(short_desc))
    
    class Meta:
        verbose_name = _('System Type')
        verbose_name_plural = _('System types')
        ordering = ('name',)
        
class SystemTypeMaintenance(models.Model):
    
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
    system_type = models.ForeignKey(SystemType)
    system_type.verbose_name = _('System')
    
    work_type = models.CharField(max_length = 2, choices = WORK_TYPE, default = 'WH')
    work_type.verbose_name = _('Maintenance type')

    # what to do
    work_description = models.TextField(_('Work description'))
    
    # when to do the job
    work_cycle_count = models.IntegerField(_('Maintenance done every'), default = 1)
    work_cycle = models.CharField(max_length = 2, choices = WORK_CYCLE, default = 'WH')
    work_cycle.verbose_name = _('Time periods')

    # model overides
    def __unicode__(self):
        short_desc = self.work_description.split()[:5]
        
        return '%s' % (' '.join(short_desc))
        
    def save(self, *args, **kwargs):
        self.work_type = self.work_cycle
        
        # call the default save method
        super(SystemTypeMaintenance, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('System Type Maintenance')
        verbose_name_plural = _('System Type Maintenance')
        ordering = ('system_type',)
    





