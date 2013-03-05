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

from mro_order.models import Order
from mro_system.models import System, Maintenance
from mro_contact.models import Employee

class OrderTable(tables.Table):
    name = tables.TemplateColumn(
        '<a href="/order/fracture/{{ record.system.pk }}/{{ record.pk }}/" >{{ record }}</a>')
    name.verbose_name = _('Description')
    name.orderable = False

    class Meta:
        model = Order
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'work_order_state', 
            'priority', 
            'assign_to', 
            'assign_to_suplier',
            'created', 
            'assigned', 
            'completed',)

class AllOrderTable(tables.Table):
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
            'assign_to', 
            'assign_to_suplier',
            'created', 
            'assigned', 
            'completed',)

class MaintenanceOrderTable(tables.Table):
    name = tables.TemplateColumn(
        '<a href="/order/maintenance/{{ record.system.pk }}/{{ record.pk }}/" >{{ record }}</a>')
    name.verbose_name = _('Description')
    name.orderable = False

    class Meta:
        model = Order
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}

        fields = (
            'work_order_state', 
            'priority', 
            'assign_to', 
            'assign_to_suplier',
            'created', 
            'assigned', 
            'completed',)

class SystemTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
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
            'department',
            'short_description',
            'last_maintenance',
            'card_number',
            'contract_number',
            'contract_include_parts',)

class MaintenanceTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    action = tables.TemplateColumn(
        '<a class="btn btn-primary" href="/order/maintenance/{{ record.system.pk }}/add/{{ record.pk }}/" >%s</a>' % _('Issue work order'))
    action.verbose_name = u'  '

    system = tables.TemplateColumn(
        '{{ record }}')
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
            'priority', 
            'work_cycle_str', 
            'estimated_work_time', 
            'last_maintenance',
            'current_counter_value',
            'last_maintenance_counter_value',
            'action',)
