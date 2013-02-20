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
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.shortcuts import render, render_to_response
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from django_tables2 import RequestConfig

from mro_system.models import Maintenance, System
from mro_contact.models import Department, Employee, Suplier
from mro_order.models import Order, OrderItem, OrderEmployee
from mro_order.tables import OrderTable
from mro_order.forms import OrderForm

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/order/',
    'image_url': '/static/tango/150x150/status/awaiting-plus.png',
    'name': ugettext_noop('Work Orders'),
    'description': ugettext_noop('Edit and add work orders.'), 
}

# views
def work(request):
    '''
    '''
    
    thumbs = [
        {   'link': '/order/maintenance/',
            'image_url': '/static/tango/150x150/status/flag-green-clock.png',
            'name': ugettext_noop('Maintenance'),
            'description': ugettext_noop('Edit and create maintenance orders.'), 
        }, {
            'link': '/order/fracture/',
            'image_url': '/static/tango/150x150/status/flag-red-clock.png',
            'name': ugettext_noop('Fracture'),
            'description': ugettext_noop('Edit and create fracture maintenance orders.'), 
        },
    ]
    
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Work orders'),
        'lead': _('Edit and add work orders.'),
        'thumb': '/static/tango/48x48/status/awaiting-plus.png',
    }
    
    response_dict['thumbs'] = thumbs
    
    return render(request, 'mro/base_list.html', response_dict)

def work_maintenance(request):
    '''
    '''
    
    departments = Department.objects.all()

    response_dict = {}
    response_dict['headers'] = {
        'header': _('Schedual Maintenance'),
        'lead': _('Edit and create schedual maintenance work orders.'),
        'thumb': '/static/tango/48x48/status/flag-green-clock.png',
    }
    response_dict['thumbs'] = departments
    
    return render(request, 'mro/base_thumbs.html', response_dict)

def work_fracture(request):
    '''
    '''
    
    departments = Department.objects.all()
    
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Fracture Maintenance'),
        'lead': _('Edit and create fracture maintenance work orders.'),
        'thumb': '/static/tango/48x48/status/flag-red-clock.png',
    }
    response_dict['thumbs'] = departments
    
    return render(request, 'mro/base_thumbs.html', response_dict)

def order_table(request, department_pk = None, order_id = None, action = None, work_type = 'fracture'):
    """
    """
    # get the employee data from the data base
    objs = Order.objects.all().order_by('created','assigned','completed')
    
    objs &= Order.objects.filter(equipment__department = department_pk)
    objs &= Order.objects.filter(work_type = ['MA', 'FR'][work_type == 'fracture'])
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        
        objs &= Order.objects.filter(assign_to__name__icontains = search)
        objs |= Order.objects.filter(equipment__name___icontains = search)
        objs |= Order.objects.filter(work_description___icontains = search)
        objs |= Order.objects.filter(work_notes___icontains = search)
    
    # create a table object for the employee data
    table = OrderTable(objs)
    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search
    response_dict['filters'] = None
    
    response_dict['table'] = table
    response_dict['add_action'] = True
    
    thumbs = [
        {   'thumb': '/static/tango/150x150/status/flag-green-clock.png',
            'header': _('Maintenance'),
            'lead': _('Edit and create maintenance orders.'), 
        }, {
            'thumb': '/static/tango/150x150/status/flag-red-clock.png',
            'header': _('Fracture'),
            'lead': _('Edit and create fracture maintenance orders.'), 
        },
    ]
    response_dict['headers'] = thumbs[work_type == 'fracture']
    
    return render(request, 'mro/base_table.html', response_dict)

def manage_order(request, department_pk = None, order_id = None, action = None, work_type = 'fracture'):
    if  order_id == None:
        order = Order(work_type = ['MA', 'FR'][work_type == 'fracture'])
    else:
        try:
            order = Order.objects.get(id = order_id)
        except:
            order = Order(work_type = ['MA', 'FR'][work_type == 'fracture'])

    ItemFormSet    = inlineformset_factory(Order, OrderItem, extra = 2, can_delete=True)
    queryset = OrderItem.objects.all() 

    EmployeeFormSet    = inlineformset_factory(Order, OrderEmployee, extra = 2, can_delete=True)
    employeequeryset = OrderEmployee.objects.all() 

    redirect_url = '/order/%s/' % (work_type)

    if request.method == "POST":
        action = request.POST['form-action']

        if action == '_delete':
            order.delete()
            return HttpResponseRedirect(redirect_url)

        orderform = OrderForm(request.POST, instance=order)

        itemformset = ItemFormSet(request.POST, request.FILES, instance=order)
        employeeformset = EmployeeFormSet(request.POST, request.FILES, instance=order)
        
        if orderform.is_valid() and itemformset.is_valid() and employeeformset.is_valid():
            orderform.save()
            itemformset.save()
            employeeformset.save()

            # Redirect to somewhere
            try:
                redirect_url = '/order/%s/%s/' % (
                    ['maintenance','fracture'][order.work_type == 'FR'], 
                    order.equipment.department.pk)
            except:
                pass
            
            if action == '_save':
                return HttpResponseRedirect(redirect_url)
            if action == '_update':
                return HttpResponseRedirect('/order/%d' % order.pk)

            if '_addanother' in request.POST:
                return HttpResponseRedirect(redirect_url)

            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request, _('Error updating database.'))

            orderform = OrderForm(instance=order)
            itemformset = ItemFormSet(instance=order, queryset=queryset)
            employeeformset = EmployeeFormSet(instance=order, queryset=employeequeryset)
    else:
        orderform = OrderForm(instance=order)
        itemformset = ItemFormSet(instance=order, queryset=queryset)
        employeeformset = EmployeeFormSet(instance=order, queryset=employeequeryset)

    response_dict = {}
    response_dict['headers'] = {
        'header': _('Maintenanace order'),
        'lead': _('Edit maintenanace order.'),
        'thumb': '/static/tango/48x48/actions/log-in.png',
    }
    response_dict['form'] = orderform
    response_dict['formset'] = itemformset
    response_dict['employeeformset'] = employeeformset

    return render(request, 'mro_order/manage_order_items.html', response_dict)

