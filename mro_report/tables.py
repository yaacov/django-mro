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
    
    name = tables.TemplateColumn(
        '<a href="{{ record.pk }}/" >{{ record.name }}</a>')
    name.verbose_name = _('System Name')

    short_description = tables.TemplateColumn(
        '{{ record }}', orderable=False)
    short_description.verbose_name = _('Description')

    class Meta:
        model = System
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'name',
            'suplier',
            'department',
            'short_description',
            'last_maintenance',
            'card_number',
            'contract_number',
            'contract_include_parts', 
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
            'priority', 
            'work_cycle_str', 
            'estimated_work_time', 
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

class SystemOrderTable(tables.Table):
    name = tables.TemplateColumn(
        '''<a href="/order/{% if record.maintenance %}maintenance{% else %}fracture{% endif %}/{{ record.system.pk }}/{{ record.pk }}/" >{{ record }}</a>''')
    name.verbose_name = _('Description')
    name.orderable = False

    order_a = tables.TemplateColumn(
        '{% if record.maintenance %}<span class="maintenance">' + 
            _('Maintenance') + '</span>{% else %}<span class="fracture">' + 
            _('Fracture') + '</span>{% endif %}')

    order_a.verbose_name = _('Order type')
    order_a.orderable = False

    class Meta:
        model = Order
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'order_a',
            'work_order_state', 
            'priority', 
            'assign_to', 
            'assign_to_suplier',
            'created', 
            'assigned', 
            'completed',)

class EmployeeOrderTable(tables.Table):
    name = tables.TemplateColumn(
        '''<a href="/order/{% if record.maintenance %}maintenance{% else %}fracture{% endif %}/{{ record.system.pk }}/{{ record.pk }}/" >{{ record }}</a>''')
    name.verbose_name = _('Description')
    name.orderable = False

    order_a = tables.TemplateColumn(
        '{% if record.maintenance %}<span class="maintenance">' + 
            _('Maintenance') + '</span>{% else %}<span class="fracture">' + 
            _('Fracture') + '</span>{% endif %}')

    order_a.verbose_name = _('Order type')
    order_a.orderable = False

    class Meta:
        model = Order
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'system',
            'order_a',
            'work_order_state', 
            'priority', 
            'assign_to_suplier',
            'created', 
            'assigned', 
            'completed',)

class EmployeeTable(tables.Table):
    first_name = tables.TemplateColumn(
        '<a href="{{ record.pk }}/" >{{ record.first_name }}</a>')
    
    department_list = tables.Column(accessor='department_list', orderable=False)
    department_list.verbose_name = _('Departments')
    
    phone = tables.TemplateColumn(
        '<a href="tel:{{ value }}/" >{{ value }}</a>')
    phone.verbose_name = _('Phone')
    
    cell_phone = tables.TemplateColumn(
        '<a href="tel:{{ value }}/" >{{ value }}</a>')
    cell_phone.verbose_name = _('Cell phone')
    
    class Meta:
        model = Employee
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'first_name', 'last_name',
            'department_list', 
            'phone', 
            'cell_phone', 
            'address', 
            'email')
