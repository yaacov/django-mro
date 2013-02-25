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
        '{{ record.name }}')
    name.verbose_name = _('Name')
    
    short_description = tables.TemplateColumn(
        '<a href="/system/{{ record.pk }}/" >{{ record }}</a>', orderable=False)
    short_description.verbose_name = _('Description')

    last_maintenance = tables.TemplateColumn(
        '{{ record.maintenance }}', orderable=False)
    last_maintenance.verbose_name = _('Description')

    class Meta:
        model = System
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'name',
            'department',
            'short_description',
            'last_maintenance',
            'serial_number', 
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
            'priority', 
            'work_cycle_str', 
            'estimated_work_time', 
            'last_maintenance')
