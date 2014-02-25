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
# Author: Yaacov Zamir 2013) <kobi.zamir@gmail.com>

from datetime import datetime, date, timedelta

from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from django_tables2   import RequestConfig

from mro_system.models import System, Maintenance, Item, MaintenanceItem, SystemDocument,Equipment
from mro_contact.models import Department, Employee

from mro_system.tables import SystemTable, EquipmentTable
from mro_system.tables import MaintenanceTable

from mro_system.forms import SystemForm, MaintenanceForm, SystemMaintenanceForm, EquipmentForm
#from mro_system_type.models import SystemType,SystemTypeMaintenance

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/equipment/system',
    'image_url': '/static/tango/150x150/actions/load-settings.png',
    'name': ugettext_noop('Maintenance Cards'),
    'description': ugettext_noop('Manage Equipment maintenance cards.'), 
}

from mro_system.management.commands.check_maintenance_schedual import Command as CheckCron
from mro_system.management.commands.read_system_counter import Command as CheckReaders

def run_cron(request):
    '''
    '''

    # check for date
    date_today_str = request.GET.get('date', None)
    date_today = date.today()
    run = False

    if date_today_str:
        try:
            date_today = datetime.strptime(date_today_str, "%d/%m/%Y").date()
        except Exception, e:
            print e
            pass

        # chedk for new actions
        check = CheckCron()
        check.handle(date_today = date_today)

        # read counters
        check = CheckReaders()
        check.handle()

        run = True

    response_dict = {}
    response_dict['headers'] = {
        'header': "",
        'lead':  "",
        'thumb': '/static/tango/48x48/status/flag-green-clock.png',
    }
    response_dict['content'] = '''
    <div dir="ltr">
    <p>Run daily reading of counters, and issue new work orders.</p>
    <form>
    date:<br>
    <input id="id_date" type="text" name="date" value="%s" ></input><br>
    <button type="submit">Run</button>
    </form>
    </div>
    <script>
    $('#id_date').datepicker({'format': 'dd/mm/yyyy'});
    </script>
    Success - %s''' % (date_today.strftime("%d/%m/%Y"), run)

    return render(request, 'mro/base.html', response_dict)

