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

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/contact/',
    'image_url': '/static/tango/150x150/categories/user-group.png',
    'name': ugettext_noop('Contacts'),
    'description': ugettext_noop('Manage suppliers and employees. Add and edit contact information for suppliers and employees.'), 
}

# views
def contact(request):
    ''' contact application main view
        
        chose between supliers and employees
    '''
    
    response_dict = {
        'headers': {
            'header': _('Contacts'),
            'lead': _('Manage suppliers and employees. Add and edit contact information for suppliers and employees.'),
            'thumb': '/static/tango/48x48/categories/user-group.png',
        },
        'thumbs': [
            #{   'link': '/contact/supliers/',
            #    'image_url': '/static/tango/48x48/categories/user-organisational-unit.png',
            #    'name': ugettext_noop('Supliers'),
            #    'description': ugettext_noop('Manage supliers contact information. Add and edit supliers.'), 
            #}, 
            {
                'link': '/contact/employees/',
                'image_url': '/static/tango/48x48/categories/user-employee.png',
                'name': ugettext_noop('Employees'),
                'description': ugettext_noop('Manage employees contact information. Add and edit employees.'), 
            },
        ],
    }
    
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
        objs |= Employee.objects.filter(phone__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= Employee.objects.filter(departments__in = filter_pk)
        filter_string = Department.objects.get(pk = filter_pk)
    
    if not filter_string:
        filter_string = _('All')
    
    # create a table object for the employee data
    table = EmployeeTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Employees contact information list'),
            'lead': None,
            'thumb': '/static/tango/48x48/categories/user-employee.png',
        },
        'search': search,
        'filters': Department.objects.all(),
        'current_filter_pk': filter_pk,
        'current_filter_string': filter_string,
        
        'table': table,
        'add_action': True,
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
            return HttpResponseRedirect('/contact/employees/') # Redirect after POST
        
        # save / update ?
        form = EmployeeForm(request.POST, request.FILES, instance = employee) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            
            if request.POST.get('submit'):
                return HttpResponseRedirect('/contact/employees/') # Redirect after POST
    else:
        form = EmployeeForm(instance = employee)
    
    response_dict = {
        'headers': {
            'header': _('Manage employee contact information.'),
            'lead': None,
            'thumb': '/static/tango/48x48/categories/user-employee.png',
        },
        'form': form,
        'table': None,
    }
    
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
        objs |= Suplier.objects.filter(contact_name__icontains = search)
        objs |= Suplier.objects.filter(phone__icontains = search)

    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= Suplier.objects.filter(departments__in = filter_pk)
        filter_string = Department.objects.get(pk = filter_pk)
    
    if not filter_string:
        filter_string = _('All')
    
    # create a table object for the employee data
    table = SuplierTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    response_dict = {
        'headers': {
            'header': _('Supliers contact information list'),
            'lead': None,
            'thumb': '/static/tango/48x48/categories/user-organisational-unit.png',
        },
        'search': search,
        'filters': Department.objects.all(),
        'current_filter_pk': filter_pk,
        'current_filter_string': filter_string,
        
        'table': table,
        'add_action': True,
    }
    
    return render(request, 'mro_contact/base_table.html', response_dict)

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
            return HttpResponseRedirect('/contact/supliers/') # Redirect after POST
        
        # save / update ?
        form = SuplierForm(request.POST, request.FILES, instance = suplier) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            
            if request.POST.get('submit'):
                return HttpResponseRedirect('/contact/supliers/') # Redirect after POST
    else:
        form = SuplierForm(instance = suplier)
        
    response_dict = {
        'headers': {
            'header': _('Manage suplier contact information.'),
            'lead': None,
            'thumb': '/static/tango/48x48/categories/user-organisational-unit.png',
        },
        'form': form,
        'table': None,
    }
    
    return render(request, 'mro_contact/base_form.html', response_dict)
    
