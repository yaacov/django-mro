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
from django.conf import settings

from django_tables2   import RequestConfig

from mro_contact.models import Department
from mro_contact.models import Employee, Suplier
from mro_contact.forms import EmployeeForm, SuplierForm
from mro_contact.tables import EmployeeTable, SuplierTable

# init a default response_dict
response_dict = {}

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/contacts/',
    'image_url': '/static/tango/150x150/categories/users.png',
    'name': ugettext_noop('Contacts'),
    'description': ugettext_noop('Edit and add suppliers and employees.'), 
}

# views
def contact(request):
    '''
    '''
    
    thumbs = [
        {   'link': '/contacts/supliers/',
            'image_url': '/static/tango/150x150/categories/user-organisational-unit.png',
            'name': ugettext_noop('Supliers'),
            'description': ugettext_noop('Edit and create supliers contacts.'), 
        }, {
            'link': '/contacts/employees/',
            'image_url': '/static/tango/150x150/categories/user-employee.png',
            'name': ugettext_noop('Employees'),
            'description': ugettext_noop('Edit and create employees contacts.'), 
        },
    ]
    
    response_dict['headers'] = {
        'header': _('Contacts'),
        'lead': _('Edit and add suppliers and employees.'),
        'thumb': '/static/tango/48x48/categories/users.png',
    }
    
    response_dict['thumbs'] = thumbs
    
    return render(request, 'mro_contact/base_list.html', response_dict)

def contact_employees(request):
    '''
    '''
    
    # get the employee data from the data base
    objs = Employee.objects.all()
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        
        objs &= Employee.objects.filter(first_name__icontains = search)
        objs |= Employee.objects.filter(last_name__icontains = search)
        objs |= Employee.objects.filter(email__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= Employee.objects.filter(departments__in = filter_pk)
        filter_string = Department.objects.get(pk = filter_pk)
    
    if not filter_string:
        filter_string = _('All')
    
    # create a table object for the employee data
    table = EmployeeTable(objs)
    RequestConfig(request, paginate={"per_page": 45}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict['search'] = search
    response_dict['filters'] = Department.objects.all()
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string
    
    response_dict['table'] = table
    response_dict['add_action'] = True
    
    response_dict['headers'] = {
        'header': _('Employees list'),
        'lead': None,
        'thumb': '/static/tango/48x48/categories/user-employee.png',
    }
    
    return render(request, 'mro_contact/base_table.html', response_dict)

def contact_employees_edit(request, num = None):
    '''
    '''
    try:
        employee = Employee.objects.get(pk = num)
    except:
        employee = Employee()
        
    if request.method == 'POST': # If the form has been submitted...
        # delete ?
        if request.POST.get('delete'):
            try:
                employee.delete()
            except:
                pass
            return HttpResponseRedirect('/contacts/employees/') # Redirect after POST
        
        # save / update ?
        form = EmployeeForm(request.POST, request.FILES, instance = employee) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            
            if request.POST.get('submit'):
                return HttpResponseRedirect('/contacts/employees/') # Redirect after POST
    else:
        form = EmployeeForm(instance = employee)
    
    response_dict['headers'] = {
        'header': _('Edit employee contact info'),
        'lead': None,
        'thumb': '/static/tango/48x48/categories/user-employee.png',
    }
    
    response_dict['form'] = form
    response_dict['table'] = None
    
    return render(request, 'mro_contact/base_form.html', response_dict)

def contact_supliers(request):
    '''
    '''
    
    # get the employee data from the data base
    objs = Suplier.objects.all()
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        
        objs &= Suplier.objects.filter(name__icontains = search)
        objs |= Suplier.objects.filter(email__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= Suplier.objects.filter(departments__in = filter_pk)
        filter_string = Department.objects.get(pk = filter_pk)
    
    if not filter_string:
        filter_string = _('All')
    
    # create a table object for the employee data
    table = SuplierTable(objs)
    RequestConfig(request, paginate={"per_page": 45}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict['search'] = search
    response_dict['filters'] = Department.objects.all()
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string
    
    response_dict['table'] = table
    response_dict['add_action'] = True
    
    response_dict['headers'] = {
        'header': _('Supliers list'),
        'lead': None,
        'thumb': '/static/tango/48x48/categories/user-organisational-unit.png',
    }
    
    return render(request, 'mro/base_table.html', response_dict)

def contact_supliers_edit(request, num = None):
    '''
    '''
    
    try:
        suplier = Suplier.objects.get(pk = num)
    except:
        suplier = Suplier()
        
    if request.method == 'POST': # If the form has been submitted...
        # delete ?
        if request.POST.get('delete'):
            try:
                suplier.delete()
            except:
                pass
            return HttpResponseRedirect('/contacts/supliers/') # Redirect after POST
        
        # save / update ?
        form = SuplierForm(request.POST, request.FILES, instance = suplier) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            
            if request.POST.get('submit'):
                return HttpResponseRedirect('/contacts/supliers/') # Redirect after POST
    else:
        form = SuplierForm(instance = suplier)
    
    response_dict['headers'] = {
        'header': _('Edit suplier contact info'),
        'lead': None,
        'thumb': '/static/tango/48x48/categories/user-organisational-unit.png',
    }
    
    response_dict['form'] = form
    response_dict['table'] = None
    
    return render(request, 'mro_contact/base_form.html', response_dict)
    
