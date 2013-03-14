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
from django import forms
from django.contrib import admin

from mro_contact.models import Department, Employee

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]

admin.site.register(Department, DepartmentAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department_list', 'phone', 'cell_phone', 'email',)
    search_fields = ['first_name', 'last_name',]
    list_editable = None
    list_filter = ('departments',)
    
    fieldsets = (
        (None, {
            'fields': (
                'first_name', 
                'last_name',
                'phone', 
                'cell_phone',
                'address', 
                'email',
                'image', 
                'departments',
            )
        }),
    )

admin.site.register(Employee, EmployeeAdmin)
