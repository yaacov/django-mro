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

from django.utils.translation import ugettext as _
import django_tables2 as tables

from mro_system.models import System, Maintenance

class SystemTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    name = tables.TemplateColumn(
        '<a href="/system/{{ record.pk }}/" >{{ record.name }}</a>')
    name.verbose_name = _('System Name')
    
    #short_description = tables.TemplateColumn(
    #    '{{ record }}', orderable=False)
    #short_description.verbose_name = _('Description')
    
    has_hourly_maintenance = tables.BooleanColumn('has_hourly_maintenance', orderable=False)
    has_hourly_maintenance.verbose_name = _('Hourly')

    has_daily_maintenance = tables.BooleanColumn('has_daily_maintenance', orderable=False)
    has_daily_maintenance.verbose_name = _('Daily')

    has_weekly_maintenance = tables.BooleanColumn('has_weekly_maintenance', orderable=False)
    has_weekly_maintenance.verbose_name = _('Weekly')

    has_monthly_maintenance = tables.BooleanColumn('has_monthly_maintenance', orderable=False)
    has_monthly_maintenance.verbose_name = _('Monthly')

    has_yearly_maintenance = tables.BooleanColumn('has_yearly_maintenance', orderable=False)
    has_yearly_maintenance.verbose_name = _('Yearly')

    class Meta:
        model = System
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'name',
            'department',
            'assign_to',
            #'card_number',
            'contract_number',
            'contract_include_parts', 
            #'short_description',
            'last_maintenance',
            'has_hourly_maintenance', 
            'has_daily_maintenance', 
            'has_weekly_maintenance', 
            'has_monthly_maintenance', 
            'has_yearly_maintenance', 
            )

class MaintenanceTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    system = tables.TemplateColumn(
        '<a href="/system/{{ record.system.pk }}/maintenance/{{ record.pk }}/" >{{ record }}</a>')
    system.verbose_name = _('Maintenance Instruction')
    
    work_cycle_str = tables.TemplateColumn('{{ value }}')
    work_cycle_str.verbose_name = _('Work cycle')
    
    class Meta:
        model = Maintenance
        orderable = False
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'system', 
            #'priority', 
            'work_cycle_str', 
            'estimated_work_time', 
            'last_maintenance',
            'current_counter_value',
            'last_maintenance_counter_value')
