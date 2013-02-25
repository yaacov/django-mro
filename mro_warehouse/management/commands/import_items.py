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

import os
from django.core.management.base import BaseCommand, CommandError

from mro_warehouse.models import Item, Warehouse, WarehouseItem

class Command(BaseCommand):
    help = 'compile less files, and minify the css and js files'
    
    def handle(self, *args, **options):
        ''' run the command
        '''
        
        f = open(args[0], 'r')  
        for line in f:
            line =  line.split(';')

            try:
                name = line[0]
                amount = int(line[1])
            except:
                continue
            
            item = Item()  
            item.name = name
            item.catalogic_number = name
            item.unit = 'PC'
            
            item.save()
            
            warehouse_item = item
            warehouse_item.warehouse = Warehouse.objects.get(pk = 0)
            warehouse_item.item = item.pk
            warehouse_id.amount = amount
            
            warehouse_item.save()
            
        f.close()
