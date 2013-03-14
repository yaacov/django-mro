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

from mro_contact.models import Department
from mro_contact.models import Employee
class Command(BaseCommand):
    help = 'import contacts form csv file'
    
    def handle(self, *args, **options):
        ''' run the command
        '''
        
        delimiter = ';'

        f = open(args[0], 'r')  
        for line in f:
            line =  line.split(delimiter)

            # read csv
            try:
                name = line[4].strip('"').replace('""', '"')
                phone = line[2]
                fax = line[3]
                contact_name = line[1].strip('"').replace('""', '"')
            except:
                print 'warning: bad employee line'
                continue
            
            # check name
            if name:
                try:
                    # if supllier already in list, continue
                    employee = Employee.objects.get(last_name = name)
                    continue
                except:
                    pass
            else:
                print 'warning: bad employee name'
                continue


            # find department
            department = Department.objects.get(id = 2)

            # make the item
            employee = Employee()
            employee.last_name = name
            employee.first_name = contact_name
            employee.phone = phone
            employee.fax = fax

            try:
                employee.save()

                # add to many to many field
                employee.departments.add(department)
            except:
                print 'warning: employee %s can not enter db' % name
            
            print 'success: employee %s, updated in db' % name

        f.close()
