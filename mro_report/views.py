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

from datetime import date
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.shortcuts import render, render_to_response
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from django_tables2   import RequestConfig

from mro_warehouse.models import Item, Warehouse, WarehouseItem, WarehouseLog
from mro_system.models import System, Maintenance, Item, MaintenanceItem
from mro_order.models import OrderDocument, Order
from mro_contact.models import Employee

from mro_report.tables import WarehouseLogTable, SystemTable, MaintenanceTable, OrderDocumentTable
from mro_report.tables import SystemOrderTable, EmployeeOrderTable, EmployeeTable

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/report/',
    'image_url': '/static/tango/150x150/emblems/report-run.png',
    'name': ugettext_noop('Reports'),
    'description': ugettext_noop('Syetem reports. View and export reports.'), 
}

# views
def report(request):
    '''
    '''
    
    thumbs = [
        {
            'link': '/report/maintenance_order_employee/',
            'image_url': '/static/tango/48x48/categories/user-admin.png',
            'name': ugettext_noop('Maintenance orders report. By employee.'),
            'description': ugettext_noop('Display maintenance orders. By employee.'), 
        },
        {
            'link': '/report/maintenance_order_system/',
            'image_url': '/static/tango/48x48/actions/run.png',
            'name': ugettext_noop('Maintenance orders report. By system.'),
            'description': ugettext_noop('Display maintenance orders. By system.'), 
        },
        {
            'link': '/report/warehouse_log/',
            'image_url': '/static/tango/48x48/actions/arrange-boxes.png',
            'name': ugettext_noop('Warehouse action log report'),
            'description': ugettext_noop('Display warehouse action logs.'), 
        },
        {   'link': '/report/system_maintenance/',
            'image_url': '/static/tango/48x48/actions/manage-students.png',
            'name': ugettext_noop('Maintenance information report'),
            'description': ugettext_noop('Display maintenance information for a system.'), 
        }, {
            'link': '/report/system_document/',
            'image_url': '/static/tango/48x48/status/maintenance-time.png',
            'name': ugettext_noop('Maintenance documentation report'),
            'description': ugettext_noop('Display maintenance documentation for a system.'), 
        },
    ]
    
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Reports'),
        'lead': _('Syetem reports. View and export reports.'),
        'thumb': '/static/tango/48x48/emblems/report-run.png',
    }
    
    response_dict['thumbs'] = thumbs
    
    return render(request, 'mro/base_list.html', response_dict)

def system_document(request):
    '''
    '''
    
    # get the WarehouseLog data from the data base
    objs = System.objects.all().order_by('name')
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= System.objects.filter(name__icontains = search)
    
    # create a table object for the employee data
    table = SystemTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Maintenance documentation report'),
            'lead': _('Display maintenance documentation for a system. Chose system.'),
            'thumb': '/static/tango/48x48/status/maintenance-time.png',
        },
        'search': search,
        'filters': None,
        
        'table': table,
        'add_action': False,
    }
    
    return render(request, 'mro_report/base_table.html', response_dict)


def system_maintenance(request):
    '''
    '''

    # get the WarehouseLog data from the data base
    objs = System.objects.all().order_by('name')
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= System.objects.filter(name__icontains = search)
    
    # create a table object for the employee data
    table = SystemTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Maintenance information report'),
            'lead': _('Display maintenance information for a system. Chose system.'),
            'thumb': '/static/tango/48x48/actions/manage-students.png',
        },
        'search': search,
        'filters': None,
        
        'table': table,
        'add_action': False,
    }
    
    return render(request, 'mro_report/base_table.html', response_dict)

def warehouse_log(request):
    '''
    '''

    # get the WarehouseLog data from the data base
    objs = WarehouseLog.objects.all().order_by('-log_date', 'item')
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= WarehouseLog.objects.filter(item__name__icontains = search)
        objs |= WarehouseLog.objects.filter(item__catalogic_number__icontains = search)
    
    # create a table object for the employee data
    table = WarehouseLogTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Warehouse action log report'),
            'lead': _('Display warehouse action logs.'),
            'thumb': '/static/tango/48x48/actions/arrange-boxes.png',
        },
        'search': search,
        'filters': None,
        
        'table': table,
        'add_action': False,
    }
    
    return render(request, 'mro_report/base_table.html', response_dict)

def system_document_report(request, system_pk):
    '''
    '''
    
    # get the Maintenance data from the data base
    system = System.objects.get(pk = system_pk)
    objs = OrderDocument.objects.filter(order__system = system).order_by('-created')
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= OrderDocument.objects.filter(title__icontains = search)
        objs |= OrderDocument.objects.filter(description__icontains = search)
    
    # create a table object for the employee data
    table = OrderDocumentTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Maintenance documentation  - %(name)s') % {'name': system.name},
            'lead': _('Display maintenance documentation for %(name)s') % {'name': system.name},
            'thumb': '/static/tango/48x48/status/maintenance-time.png',
        },
        'search': search,
        'filters': None,
        
        'table': table,
        'add_action': False,
    }
    
    return render(request, 'mro_report/base_table.html', response_dict)

def system_maintenance_report(request, system_pk):
    '''
    '''
    
    # get the Maintenance data from the data base
    system = System.objects.get(pk = system_pk)
    objs = Maintenance.objects.filter(system = system).order_by('-last_maintenance')
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= Maintenance.objects.filter(work_description__icontains = search)
    
    # create a table object for the employee data
    table = MaintenanceTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Maintenance information  - %(name)s') % {'name': system.name},
            'lead': _('Display maintenance information for %(name)s') % {'name': system.name},
            'thumb': '/static/tango/48x48/actions/manage-students.png',
        },
        'search': search,
        'filters': None,
        
        'table': table,
        'add_action': False,
    }
    
    return render(request, 'mro_report/base_table.html', response_dict)

def maintenance_order_system(request):
    '''
    '''
    
    # get the WarehouseLog data from the data base
    objs = System.objects.all().order_by('name')
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= System.objects.filter(name__icontains = search)
    
    # create a table object for the employee data
    table = SystemTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Maintenance orders report'),
            'lead': _('Display maintenance orders. Chose system.'),
            'thumb': '/static/tango/48x48/actions/run.png',
        },
        'search': search,
        'filters': None,
        
        'table': table,
        'add_action': False,
    }
    
    return render(request, 'mro_report/base_table.html', response_dict)

def maintenance_order_employee(request):
    '''
    '''
    
    # get the WarehouseLog data from the data base
    objs = Employee.objects.all().order_by('first_name', 'last_name')
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= Employee.objects.filter(first_name__icontains = search)
        objs |= Employee.objects.filter(last_name__icontains = search)
    
    # create a table object for the employee data
    table = EmployeeTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Maintenance orders report'),
            'lead': _('Display maintenance orders. Chose employees.'),
            'thumb': '/static/tango/48x48/categories/user-admin.png',
        },
        'search': search,
        'filters': None,
        
        'table': table,
        'add_action': False,
    }
    
    return render(request, 'mro_report/base_table.html', response_dict)

def maintenance_order_system_report(request, system_pk):
    """
    """
    # get the employee data from the data base
    system = System.objects.get(pk = system_pk)
    objs = Order.objects.filter(system = system).order_by('-created','-assigned','-completed')
    
    # filter employees using the search form
    search = request.GET.get('search', '').strip()
    if search:
        objs &= Order.objects.filter(assign_to__first_name__icontains = search)
        objs |= Order.objects.filter(assign_to__last_name__icontains = search)
        objs |= Order.objects.filter(assign_to_suplier__name__icontains = search)
        objs |= Order.objects.filter(maintenance__work_description__icontains = search)
        objs |= Order.objects.filter(work_description__icontains = search)
        objs |= Order.objects.filter(work_notes__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= Order.objects.filter(work_order_state = filter_pk)
        try:
            filter_string = dict(Order.ORDER_STATE)[filter_pk]
        except:
            filter_string = None
    
    if not filter_string:
        filter_string = _('All')

    table = SystemOrderTable(objs)

    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search

    response_dict['filters'] = Order.ORDER_STATE
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string

    response_dict['table'] = table
    response_dict['headers'] = {
        'thumb': '/static/tango/48x48/actions/run.png',
        'header': _('System Work orders for %(name)s') % {'name': system.name},
        'lead': _('Display all the work orders. for the system - %(name)s') % {'name': system.name},
    }
    
    return render(request, 'mro_order/system_fracture_order.html', response_dict)

def maintenance_order_employee_report(request, employee_pk):
    """
    """
    # get the employee data from the data base
    employee = Employee.objects.get(pk = employee_pk)
    objs = Order.objects.filter(assign_to = employee).order_by('-created','-assigned','-completed')
    
    # filter employees using the search form
    search = request.GET.get('search', '').strip()
    if search:
        objs &= Order.objects.filter(system___name__icontains = search)
        objs |= Order.objects.filter(maintenance__work_description__icontains = search)
        objs |= Order.objects.filter(work_description__icontains = search)
        objs |= Order.objects.filter(work_notes__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= Order.objects.filter(work_order_state = filter_pk)
        try:
            filter_string = dict(Order.ORDER_STATE)[filter_pk]
        except:
            filter_string = None
    
    if not filter_string:
        filter_string = _('All')

    table = EmployeeOrderTable(objs)

    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search

    response_dict['filters'] = Order.ORDER_STATE
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string

    response_dict['table'] = table
    response_dict['headers'] = {
        'thumb': '/static/tango/48x48/categories/user-admin.png',
        'header': _('Employee Work orders for %(name)s') % {'name': employee},
        'lead': _('Display all the work orders. for the employee - %(name)s') % {'name': employee},
    }
    
    return render(request, 'mro_order/system_fracture_order.html', response_dict)
