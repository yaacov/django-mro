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

from mro_warehouse.models import Item, Warehouse, WarehouseItem

class WarehouseItemInline(admin.TabularInline):
    fields = ('item', 'shelve', 'batch', 'amount', 'entered', 'expires')
    
    model = WarehouseItem

class WarehouseAdmin(admin.ModelAdmin):
    
    inlines = (WarehouseItemInline,)

admin.site.register(Warehouse, WarehouseAdmin)

class ItemAdmin(admin.ModelAdmin):
    
    pass

admin.site.register(Item, ItemAdmin)

