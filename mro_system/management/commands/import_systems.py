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

from mro_contact.models import Department, Suplier
from mro_system.models import System, Maintenance

class Command(BaseCommand):
    help = 'import systems form csv file'
    
    def handle(self, *args, **options):
        ''' run the command
        '''
        
        delimiter = ';'

        f = open(args[0], 'r')
        serial_counter = 0
        year = 2013

        for line in f:
            serial_counter += 1
            line =  line.decode('utf-8').split(delimiter)

            # read csv
            try:
                name = line[0].strip('"').replace('""', '"')
                suplier_name = line[4].strip('"').replace('""', '"')
                card_number = line[9].strip('"').replace('""', '"')

                # make serial number unique
                serial_number = u'CA-%04d-%03d' % (year, serial_counter)

                description = u'מערכת בקרה ב %s' % name
            except Exception, e:
                print 'warning: bad system line', e
                continue
            
            # check name
            if name:
                try:
                    # if system already in list, continue
                    system = System.objects.get(name = name)
                    continue
                except:
                    pass
            else:
                print 'warning: bad system name'
                continue

            # find department
            department = Department.objects.get(id = 2)

            # find suplir
            try:
                suplier = Suplier.objects.get(name = suplier_name)
            except:
                suplier = None

            # make the item
            system = System()
            system.name = name
            system.suplier = suplier
            system.serial_number = serial_number
            system.card_number = card_number
            system.description = description
            system.department = department

            try:
                system.save()
                print 'success: system %s, updated in db' % name
            except Exception, e:
                print 'warning: system %s can not enter db, %s' % (name, e)
            
        f.close()
