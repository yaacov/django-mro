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

from mro_equipment.models import Equipment, Maintenance

class EquipmentTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    name = tables.TemplateColumn(
        '<a href="/equipment/{{ record.pk }}/" >{{ record }}</a>')
    name.verbose_name = _('Name')
    
    class Meta:
        model = Equipment
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'name', 
            'serial_number', 
            'department', 
            'phone', 
            'address')

class MaintenanceTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    equipment = tables.TemplateColumn(
        '<a href="/equipment/{{ record.equipment.pk }}/maintenance/{{ record.pk }}/" >{{ record }}</a>')
    equipment.verbose_name = _('Maintenance Instruction')
    
    work_cycle_str = tables.TemplateColumn('{{ value }}')
    work_cycle_str.verbose_name = _('Work cycle')
    
    class Meta:
        model = Maintenance
        orderable = False
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'equipment', 
            'priority', 
            'work_cycle_str', 
            'estimated_work_time', 
            'last_maintenance')

