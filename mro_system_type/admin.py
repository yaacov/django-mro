
from import_export.admin import ImportExportModelAdmin

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib import admin

from mro_system_type.models import SystemType, SystemTypeMaintenance

class SystemTypeMaintenanceInline(admin.TabularInline):
    
    model = SystemTypeMaintenance
    extra = 1

class SystemTypeAdmin(ImportExportModelAdmin):
    
    inlines = (SystemTypeMaintenanceInline,)
    
admin.site.register(SystemType, SystemTypeAdmin)
