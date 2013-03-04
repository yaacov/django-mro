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
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from mro_warehouse.models import Item, Warehouse, WarehouseItem

class Command(BaseCommand):
    help =  '''import items form csv file
        csv file columns:
        name, amount, unit price'''


    def handle(self, *args, **options):
        ''' run the command
        '''
        
        # csv delimiter
        delimiter = ';'

        # defaults used to generate the new items
        serial_counter = 0
        year = date.today().year

        # make / check the warehouse
        try:
            warehouse = Warehouse.objects.get()
        except:
            warehouse = Warehouse(name = _('Main warehouse'))
            warehouse.save()
            print 'warning: creating new warehouse'

        # read the items csv file
        f = open(args[0], 'r')
        for line in f:

            # read a new csv line
            serial_counter += 1
            line =  line.split(delimiter)

            # try to parse the line
            try:
                name = line[0]
                amount = int(line[1])
                unit_price = float(line[2])
                catalogic_number = u'CA-%04d-%03d' % (year, serial_counter)
                unit = 'PC'
            except:
                print 'warning: line %d, ' % serial_counter
                continue
            
            # make / check item
            try:
                # try to create a new item
                item = Item()
                item.name = name
                item.unit_price = unit_price
                item.catalogic_number = catalogic_number
                item.unit = unit
                
                item.save()
            except:
                # check if item already in database
                try:
                    item = Item.objects.get(catalogic_number = catalogic_number)
                except:
                    print 'warning: bad item, can not insert item %s to db ' % name
                    continue

                print 'warning: item %s already in the db' % name

            # insert the item into the warehouse
            warehouse_item = WarehouseItem()
            warehouse_item.item = item
            warehouse_item.warehouse = warehouse
            warehouse_item.amount = amount

            warehouse_item.save()
            
            print 'success: item %s, updated in warehouse' % name

        f.close()
