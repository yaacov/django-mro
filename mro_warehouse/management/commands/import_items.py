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
    help = 'import items form csv file'
    
    def handle(self, *args, **options):
        ''' run the command
        '''
        
        delimiter = ','

        f = open(args[0], 'r')  
        serial_counter = 0
        year = 2013

        for line in f:
            serial_counter += 1
            line =  line.split(delimiter)

            try:
                name = line[0]
                amount = int(line[1])
            except:
                continue
            
            # make the item
            item = Item()  
            item.name = name

            # make catalogic number unique
            item.catalogic_number = u'CA-%04d-%03d' % (year, serial_counter)

            item.unit = 'PC'
            
            try:
                item.save()
            except:
                print 'warning: item %s can not enter db' % name
                item = Item.objects.get(catalogic_number = name)

            # make the warehouse
            try:
                warehouse = Warehouse.objects.get()
            except:
                warehouse = Warehouse(name = u'מחסן ראשי')
                warehouse.save()
                print 'warning: creating new warehouse'

            # insert the item into the warehouse
            warehouse_item = WarehouseItem()
            warehouse_item.item = item
            warehouse_item.warehouse = warehouse
            warehouse_item.amount = amount
            
            warehouse_item.save()
            
            print 'success: item %s, updated in db' % name

        f.close()
