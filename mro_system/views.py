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

from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.shortcuts import render
from django_tables2   import RequestConfig

from mro_system.models import System, Maintenance
from mro_contact.models import Department, Employee, Suplier

from mro_system.tables import SystemTable
from mro_system.tables import MaintenanceTable

from mro_system.forms import SystemForm, MaintenanceForm

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/system/',
    'image_url': '/static/tango/150x150/actions/run.png',
    'name': ugettext_noop('Systems'),
    'description': ugettext_noop('Manage systems for maintenance, edit and add systems and equipment for maintenance.'), 
}

def system(request):
    '''
    '''
    
    # get the employee data from the data base
    objs = System.objects.all()
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        
        objs &= System.objects.filter(name__icontains = search)
        objs |= System.objects.filter(serial_number__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= System.objects.filter(department = filter_pk)
        filter_string = Department.objects.get(pk = filter_pk)
    
    if not filter_string:
        filter_string = _('All')
    
    # create a table object for the employee data
    table = SystemTable(objs)
    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search
    response_dict['filters'] = Department.objects.all()
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string
    
    response_dict['table'] = table
    response_dict['add_action'] = True
    
    response_dict['headers'] = {
        'header': _('System list'),
        'lead': _('Edit and add system.'),
        'thumb': '/static/tango/48x48/actions/run.png',
    }
    
    return render(request, 'mro/base_table.html', response_dict)

def manage_system(request, num = None):
    '''
    '''
    
    # try to get an system object
    try:
        system = System.objects.get(pk = num)
    except:
        system = System()
    
    # check for post data
    if request.method == 'POST': # If the form has been submitted...
        # delete ?
        if request.POST.get('delete'):
            try:
                system.delete()
            except:
                pass
            return HttpResponseRedirect('/system/') # Redirect after POST
        
        # save / update ?
        form = SystemForm(request.POST, request.FILES, instance = system) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            
            return HttpResponseRedirect('/system/') # Redirect after POST
    else:
        form = SystemForm(instance = system)
    
    response_dict = {}
    response_dict['headers'] = {
        'header': _('System'),
        'lead': _('Edit system information.'),
        'thumb': '/static/tango/48x48/actions/run.png',
    }
    
    response_dict['form'] = form
    
    # create a table object for the employee data
    if num:
        objs = Maintenance.objects.filter(system = num)
        table = MaintenanceTable(objs)
        RequestConfig(request, paginate={"per_page": 40}).configure(table)
        response_dict['table'] = table
        response_dict['table_headers'] = {
            'header': _('Maintenance for %s') % system,
            'lead': _('Edit maintenance instruction information.'),
            'thumb': '/static/tango/48x48/status/flag-green-clock.png',
        }
    else:
        response_dict['table'] = None
        
    return render(request, 'mro_system/system_form.html', response_dict)

def manage_system_delete(request, num = None):
    '''
    '''
    
    # try to get an system object
    try:
        system = System.objects.get(pk = num)
        system.delete()
    except:
        pass
    
    return HttpResponseRedirect('/system/') # Redirect after POST

def manage_system_maintenance(request, num = None, maintenance_pk = None):
    '''
    '''
    try:
        num = int(num)
        maintenance = Maintenance.objects.get(pk = maintenance_pk)
    except:
        maintenance = Maintenance()
        maintenance.system = System.objects.get(pk = num)
        
    if request.method == 'POST': # If the form has been submitted...
        # delete ?
        if request.POST.get('delete'):
            try:
                maintenance.delete()
            except:
                pass
            return HttpResponseRedirect('/system/%d/' % num) # Redirect after POST
        
        # save / update ?
        form = MaintenanceForm(request.POST, request.FILES, instance = maintenance) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            
            if request.POST.get('submit'):
                return HttpResponseRedirect('/system/%d/' % num) # Redirect after POST
    else:
        form = MaintenanceForm(instance = maintenance)
    
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Maintenance'),
        'lead': _('Edit maintenance instruction information.'),
        'thumb': '/static/tango/48x48/status/flag-green-clock.png',
    }
    
    response_dict['form'] = form
    response_dict['table'] = None
    response_dict['delete'] = True

    return render(request, 'mro/base_form.html', response_dict)

