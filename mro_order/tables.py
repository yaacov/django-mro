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
from mro_system.models import System, Maintenance, Equipment
from mro_contact.models import Employee

class AllOrderTable(tables.Table):
    name = tables.TemplateColumn(
        '''<a href="{{ record.equipment.pk }}/{{ record.pk }}/" >{{ record }}</a>''')
    name.verbose_name = _('Description')
    name.orderable = False

    order_type = tables.TemplateColumn(
        '{% if record.maintenance %}<span class="maintenance">' + 
            _('Maintenance') + '</span>{% else %}<span class="fracture">' + 
            _('Fracture') + '</span>{% endif %}')

    order_type.verbose_name = _('Order type')
    order_type.orderable = False

    estimated_time_diff = tables.TemplateColumn(
        '''{% if record.maintenance %}
                {% if record.estimated_time_diff > 0 %}
                    <span class="positive">{{ record.estimated_time_diff }}</span>
                {% else %}
                    <span class="negative">{{ record.estimated_time_diff }}</span>
                {% endif %}
            {% endif %}
        ''', orderable = False)
    estimated_time_diff.verbose_name = _('Work hours estimate differential')

    class Meta:
        model = Order
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'equipment',
            'order_type',
            #'work_order_state', 
            #'priority', 
            'assign_to', 
            'created', 
            'assigned', 
            'completed',
            'name',
            'work_time',
            'estimated_time_diff', 
            'completed_month', 'completed_year')

class AssignTable(tables.Table):
    equipment_name = tables.TemplateColumn(
        '''{{ record.equipment.name }}''')
    equipment_name.verbose_name = _('Equipment')
    equipment_name.orderable = False

    short_description = tables.TemplateColumn(
        '''<a href="{{ record.equipment.pk }}/{{ record.pk }}/" >{{ record }}</a>''')
    short_description.verbose_name = _('Description')
    short_description.orderable = False

    maintenance_work_type = tables.TemplateColumn('{{ record.maintenance.get_work_type_display }}')
    maintenance_work_type.verbose_name = _('Work type')
    maintenance_work_type.orderable = False

    department = tables.TemplateColumn(
        '''{{ record.equipment.department }}''')
    department.verbose_name = _('Department')
    department.orderable = False

    selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input": 
                                        {"onclick": "toggle(this)"}},
                                        orderable=False)

    class Meta:
        model = Order
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'selection',
            'short_description',
            'equipment_name',
            'department',
            'maintenance_work_type',
            'work_order_state', 
            'priority', 
            'assign_to', 
            'created',
            'assigned',
            'completed',
            )

class SimpleAssignTable(tables.Table):
    equipment_name = tables.TemplateColumn(
        '''{{ record.equipment.name }}''')
    equipment_name.verbose_name = _('Equipment')
    equipment_name.orderable = False

    short_description = tables.TemplateColumn(
        '''<a href="{{ record.equipment.pk }}/{{ record.pk }}/" >{{ record }}</a>''')
    short_description.verbose_name = _('Description')
    short_description.orderable = False

    maintenance_work_type = tables.TemplateColumn('{{ record.maintenance.get_work_type_display }}')
    maintenance_work_type.verbose_name = _('Work type')
    maintenance_work_type.orderable = False

    department = tables.TemplateColumn(
        '''{{ record.equipment.department }}''')
    department.verbose_name = _('Department')
    department.orderable = False

    selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input": 
                                        {"onclick": "toggle(this)"}},
                                        orderable=False)

#    contract_number = tables.TemplateColumn('{{ record.maintenance.system.contract_number }}')
#    contract_number.verbose_name = _('Contract number')
#    contract_number.orderable = False

    contract_include_parts = tables.TemplateColumn('''
        {% if record.equipment.contract_include_parts %}
        <span class="true">✔</span>
        {%else%}
        <span class="false">✘</span>
        {%endif%}''')
    contract_include_parts.verbose_name = _('Contract include parts')
    contract_include_parts.orderable = False

    class Meta:
        model = Order
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'selection',
            'short_description',
            'system_name',
            'department',
            #'system_assign_to',
#            'contract_number',
            'contract_include_parts', 
            'maintenance_work_type',
            #'work_order_state', 
            #'priority', 
            #'assign_to', 
            'created',
            )

class MaintenanceOrderTable(tables.Table):
    name = tables.TemplateColumn(
        '<a href="{{ record.pk }}/" >{{ record }}</a>')
    name.verbose_name = _('Description')
    name.orderable = False

    order_type = tables.TemplateColumn(
        '{% if record.maintenance %}<span class="maintenance">{{ record.maintenance.get_work_type_display }}</span>{% else %}<span class="fracture">' + 
            _('Fracture') + '</span>{% endif %}')

    order_type.verbose_name = _('Order type')
    order_type.orderable = False

    class Meta:
        model = Order
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}

        fields = (
            'work_order_state', 
            'order_type',
            #'priority', 
            'assign_to', 
            'created', 
            'assigned', 
            'completed',
            'name',)

#deprecated
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
            'department',
            'short_description',
#            'last_maintenance',
            #'card_number',
            #'contract_number',
            #'contract_include_parts', 
            'has_hourly_maintenance', 
            'has_daily_maintenance', 
            'has_weekly_maintenance', 
            'has_monthly_maintenance', 
            'has_yearly_maintenance',)

class EquipmentTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    name = tables.TemplateColumn(
        '<a href="{{ record.pk }}/" >{{ record.name }}</a>')
    name.verbose_name = _('Equipment Name')
    
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
        model = Equipment
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'name',
            'department',
            'short_description',
#            'last_maintenance',
            #'card_number',
            #'contract_number',
            #'contract_include_parts', 
            'has_hourly_maintenance', 
            'has_daily_maintenance', 
            'has_weekly_maintenance', 
            'has_monthly_maintenance', 
            'has_yearly_maintenance',)

class MaintenanceTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    action = tables.TemplateColumn(
        '<a class="btn btn-primary" href="add/{{ record.pk }}/" >%s</a>' % _('Issue maintenance work order'))
    action.verbose_name = u'  '

    system = tables.TemplateColumn(
        '{{ record.system.name }}')
    system.verbose_name = _('Maintenance Instruction')

    class Meta:
        model = Maintenance
        orderable = False
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'system', 
            #'priority', 
            'work_type', 
#            'last_maintenance',
            'current_counter_value',
#            'last_maintenance_counter_value',
            'action',)
