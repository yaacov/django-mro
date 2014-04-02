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

from import_export.admin import ImportExportModelAdmin

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib import admin

from mro_system.models import Priority, System, Maintenance, Equipment
from mro_system.models import MaintenanceItem, SystemDocument

try:
    from pyca.ca_com_utils import run_command
except:
    run_command = lambda s: 0.0;

class MaintenanceItemInline(admin.TabularInline):
    fields = ('item', 'amount')
    
    model = MaintenanceItem
    extra = 0
    
class MaintenanceInline(admin.TabularInline):
    
    model = Maintenance
    extra = 0

class SystemDocumentInline(admin.TabularInline):
    fields = ('title', 'created',)
    
    model = SystemDocument
    extra = 0

admin.site.register(SystemDocument)

class PriorityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Priority, PriorityAdmin)

def reset_equipment(modeladmin, request, queryset):
    for equipment in queryset:
        if equipment.counter_reset_command:
            command = equipment.counter_reset_command
        elif (equipment.counter_protocol and 
                equipment.counter_ip and 
                equipment.counter_cpu and 
                equipment.counter_reset_parameter):
            command = "%s://%s:%s/set_param=%s,1" % (equipment.counter_protocol,
                                         equipment.counter_ip,
                                         equipment.counter_cpu,
                                         equipment.counter_reset_parameter )
        else:
            continue
        run_command(command)

reset_equipment.short_description = _("Reset")

class EquipmentAdmin(ImportExportModelAdmin):
    actions = [reset_equipment]

admin.site.register(Equipment, EquipmentAdmin)

class SystemAdmin(ImportExportModelAdmin):
    
    inlines = (MaintenanceInline, SystemDocumentInline,)

admin.site.register(System, SystemAdmin)

class MaintenanceAdmin(ImportExportModelAdmin):
    
    inlines = (MaintenanceItemInline,)

admin.site.register(Maintenance, MaintenanceAdmin)

