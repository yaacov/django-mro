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
from django.db.models import Q

from mro_contact.models import Department
from mro_system.models import System, Maintenance, Equipment

try:
    from pyca.ca_com_utils import run_command
except:
    run_command = lambda s: 0.0;

class Command(BaseCommand):
    help = 'read system counters'

    def handle(self, *args, **options):
        ''' run the command
        '''

        print '\n\nReading counters:\n'

        equipments = Equipment.objects.all()
                                        #filter((Q(counter_command__isnull = True) | 
                                        #       Q(counter_command__exact = '')) &
                                        #       Q(counter_protocol__isnull = True))

        for equipment in equipments:
            if equipment.counter_command:
                command = equipment.counter_command
            elif equipment.counter_protocol:
                command = "%s://%s:%s/get_param=%s" % (equipment.counter_protocol,
                                         equipment.counter_ip,
                                         equipment.counter_cpu,
                                         equipment.counter_parameter )
            else:
                continue
        
            print 'equipment - %s' % equipment.name
            print '    system - %s' % equipment.system.name
#            print '    last maintenance value - %f' % equipment.last_maintenance_counter_value
#            print '    current value - %f' % equipment.current_counter_value
            print '    command - %s' % command

            try:
                value = float(run_command(command).split(',')[0])
                value = int(value * 100.0) / 100.0

                equipment.current_counter_value = value
                equipment.save()
            except Exception, e:
                print '        error running command', e

            print '        new value - %f' % equipment.current_counter_value
    
    def handle_old(self, *args, **options):
        ''' run the command
        '''
        
        print '\n\nReading counters:\n'

        maintenances = Maintenance.objects.exclude(Q(counter_command__isnull = True) | Q(counter_command__exact = ''))

        for maintenance in maintenances:
            print 'system - %s' % maintenance.system.name
            print '    last maintenance value - %f' % maintenance.last_maintenance_counter_value
            print '    current value - %f' % maintenance.current_counter_value
            print '    command - %s' % maintenance.counter_command

            try:
                command = maintenance.counter_command
                value = float(run_command(command).split(',')[0])
                value = int(value * 100.0) / 100.0

                maintenance.current_counter_value = value
                maintenance.save()
            except Exception, e:
                print '        error running command', e
            
            print '        new value - %f' % maintenance.current_counter_value
