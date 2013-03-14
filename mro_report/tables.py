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

from mro_warehouse.models import WarehouseLog
from mro_system.models import System, Maintenance
from mro_order.models import OrderDocument, Order
from mro_contact.models import Employee

class WarehouseLogTable(tables.Table):
    
    class Meta:
        model = WarehouseLog
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'item', 'action', 'amount', 
            'shelve', 'batch', 'notes',
            'expires', 'log_date')

class SystemTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
   
    name = tables.TemplateColumn(
        '<a href="{{ record.pk }}/" >{{ record.name }}</a>')
    name.verbose_name = _('System Name')

    short_description = tables.TemplateColumn(
        '{{ record }}', orderable=False)
    short_description.verbose_name = _('Description')
    
    has_hourly_maintenance = tables.BooleanColumn('has_hourly_maintenance')
    has_hourly_maintenance.verbose_name = _('Hourly')

    has_daily_maintenance = tables.BooleanColumn('has_daily_maintenance')
    has_daily_maintenance.verbose_name = _('Daily')

    has_weekly_maintenance = tables.BooleanColumn('has_weekly_maintenance')
    has_weekly_maintenance.verbose_name = _('Weekly')

    has_monthly_maintenance = tables.BooleanColumn('has_monthly_maintenance')
    has_monthly_maintenance.verbose_name = _('Monthly')

    has_yearly_maintenance = tables.BooleanColumn('has_yearly_maintenance')
    has_yearly_maintenance.verbose_name = _('Yearly')

    class Meta:
        model = System
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'name',
            'assign_to',
            'department',
            'short_description',
            'last_maintenance',
            #'card_number',
            #'contract_number',
            #'contract_include_parts', 
            'has_hourly_maintenance', 
            'has_daily_maintenance', 
            'has_weekly_maintenance', 
            'has_monthly_maintenance', 
            'has_yearly_maintenance', 
            )

class MaintenanceTable(tables.Table):
    system = tables.TemplateColumn(
        '{{ record.work_description|linebreaks }}')
    system.verbose_name = _('Maintenance Instruction')
    system.orderable = False

    work_cycle_str = tables.TemplateColumn('{{ value }}')
    work_cycle_str.verbose_name = _('Work cycle')
    work_cycle_str.orderable = False

    class Meta:
        model = Maintenance
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'system', 
            'work_type',
            #'priority', 
            'work_cycle_str', 
            'last_maintenance',
            'current_counter_value',
            'last_maintenance_counter_value')

class OrderDocumentTable(tables.Table):

    description = tables.TemplateColumn(
        '{{ record.description|linebreaks }}')
    description.orderable = False

    class Meta:
        model = OrderDocument
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = ('title', 'description', 'created', 'image',)
