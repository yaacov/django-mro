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
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.db.models import Max

from mro_contact.models import Department
from mro_system.models import System, Maintenance, MaintenanceItem
from mro_order.models import Order, OrderItem

try:
    from pyca.ca_com_utils import run_command
except:
    run_command = lambda s: 0.0;

class Command(BaseCommand):
    help = 'check maintenance schedual and create work orders'
    
    def create_order(self, maintenance):

        # if a work order is pending do set a new work order
        wait_before_new_order = 7
        waiting_order = Order.objects.filter(maintenance = maintenance).exclude(work_order_state = 'CO').order_by('created')
        if (waiting_order and 
            waiting_order[0].created and
            waiting_order[0].created > (date.today() - timedelta(days = wait_before_new_order))):

            print '            work order waiting ... '
            return

        max_order = Order.objects.all().aggregate(Max('work_number'))
        if max_order['work_number__max']:
            work_number = max_order['work_number__max'] + 1
        else:
            work_number = 1

        order = Order(
            work_number = work_number,
            maintenance = maintenance,
            system = maintenance.system,
            priority = maintenance.priority,
            work_description = maintenance.work_description,
            contract_number = maintenance.system.contract_number,
            contract_include_parts = maintenance.system.contract_include_parts,
            assign_to = maintenance.system.assign_to,
        )

        order.save()

        for maintenanceitem in MaintenanceItem.objects.filter(maintenance = maintenance):
            orderitem = OrderItem(
                order = order, 
                item = maintenanceitem.item,
                amount = maintenanceitem.amount,
                ordered = date.today(),
            )
            orderitem.save()

        print '            new work order issued '

    def handle(self, *args, **options):
        ''' run the command
        '''
        
        print '\n\nCheck maintenance scheduals:\n'

        # daily 
        print "\nDaily maintenances"
        maintenances = Maintenance.objects.filter(work_cycle = 'DA')

        for maintenance in maintenances:
            print 'system - %s' % maintenance.system.name
            print '    days between maintenances - %d' % maintenance.work_cycle_count

            if not maintenance.last_maintenance:
                print '    never done'

                # schedual work order
                print '        Issue new work order'
                self.create_order(maintenance)
            else:
                diff = (date.today() - maintenance.last_maintenance).days
                cycle_count = maintenance.work_cycle_count

                print '    last maintenance - %s' % maintenance.last_maintenance
                print '    days since last maintenance - %d' % diff

                if diff > cycle_count:
                    # schedual work order
                    print '        Issue new work order'
                    self.create_order(maintenance)

        # daily 
        print "\nWeekly maintenances"
        maintenances = Maintenance.objects.filter(work_cycle = 'WE')

        for maintenance in maintenances:
            print 'system - %s' % maintenance.system.name
            print '    weeks between maintenances - %d' % maintenance.work_cycle_count

            if not maintenance.last_maintenance:
                print '    never done'

                # schedual work order
                print '        Issue new work order'
                self.create_order(maintenance)
            else:
                diff = (date.today() - maintenance.last_maintenance).days / 7
                cycle_count = maintenance.work_cycle_count

                print '    last maintenance - %s' % maintenance.last_maintenance
                print '    weeks since last maintenance - %d' % diff

                if diff > cycle_count:
                    # schedual work order
                    print '        Issue new work order'
                    self.create_order(maintenance)

        # monthly 
        print "\nMonthly maintenances"
        maintenances = Maintenance.objects.filter(work_cycle = 'MO')

        for maintenance in maintenances:
            print 'system - %s' % maintenance.system.name
            print '    months between maintenances - %d' % maintenance.work_cycle_count

            if not maintenance.last_maintenance:
                print '    never done'

                # schedual work order
                print '        Issue new work order'
                self.create_order(maintenance)
            else:
                date1 = maintenance.last_maintenance
                date2 = date.today()
                m1 = date1.year * 12 + date1.month
                m2 = date2.year * 12 + date2.month
                diff = m2 - m1
                if date1.day > date2.day:
                    diff -= 1
                cycle_count = maintenance.work_cycle_count

                print '    last maintenance - %s' % maintenance.last_maintenance
                print '    months since last maintenance - %d' % diff

                if diff > cycle_count:
                    # schedual work order
                    print '        Issue new work order'
                    self.create_order(maintenance)

        # yearly 
        print "\nYearly maintenances"
        maintenances = Maintenance.objects.filter(work_cycle = 'YE')

        for maintenance in maintenances:
            print 'system - %s' % maintenance.system.name
            print '    years between maintenances - %d' % maintenance.work_cycle_count

            if not maintenance.last_maintenance:
                print '    never done'

                # schedual work order
                print '        Issue new work order'
                self.create_order(maintenance)
            else:
                date1 = maintenance.last_maintenance
                date2 = date.today()
                m1 = date1.year * 12 + date1.month
                m2 = date2.year * 12 + date2.month
                diff = m2 - m1
                if date1.day > date2.day:
                    diff -= 1
                diff = diff / 12
                cycle_count = maintenance.work_cycle_count

                print '    last maintenance - %s' % maintenance.last_maintenance
                print '    years since last maintenance - %d' % diff

                if diff > cycle_count:
                    # schedual work order
                    print '        Issue new work order'
                    self.create_order(maintenance)

        # yearly 
        print "\nWork hour maintenances"
        maintenances = Maintenance.objects.filter(work_cycle = 'WH')

        for maintenance in maintenances:
            print 'system - %s' % maintenance.system.name
            print '    work hours between maintenances - %d' % maintenance.work_cycle_count

            if not maintenance.last_maintenance:
                print '    never done'

                # schedual work order
                print '        Issue new work order'
                self.create_order(maintenance)
            else:
                diff = maintenance.current_counter_value - maintenance.last_maintenance_counter_value
                cycle_count = maintenance.work_cycle_count

                print '    last maintenance - %s' % maintenance.last_maintenance
                print '    current counter - %s' % maintenance.current_counter_value
                print '    last maintenance counter - %s' % maintenance.last_maintenance_counter_value
                print '    work hours since last maintenance - %d' % diff

                if diff > cycle_count:
                    # schedual work order
                    print '        Issue new work order'
                    self.create_order(maintenance)
