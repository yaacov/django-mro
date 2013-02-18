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

from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables

from mro_contact.models import Employee, Suplier

class EmployeeTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    name = tables.TemplateColumn(
        '<a href="{{ record.pk }}/" >{{ record }}</a>')
    name.verbose_name = _('Name')
    
    department_list = tables.Column(accessor='department_list')
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
            'name', 
            'department_list', 
            'phone', 
            'cell_phone', 
            'address', 
            'email')

class SuplierTable(tables.Table):
    #image = tables.TemplateColumn('<img src="{{ record.image.url }}" width="100" height="100" alt="value">')
    name = tables.TemplateColumn(
        '<a href="{{ record.pk }}/" >{{ record }}</a>')
    name.verbose_name = _('Name')
    
    department_list = tables.Column(accessor='department_list')
    department_list.verbose_name = _('Departments')
    
    phone = tables.TemplateColumn(
        '<a href="tel:{{ value }}/" >{{ value }}</a>')
    phone.verbose_name = _('Phone')
    
    class Meta:
        model = Employee
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = (
            'name', 
            'department_list', 
            'phone', 
            'fax', 
            'address', 
            'email')
            
