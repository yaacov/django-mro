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

from django_tables2 import RequestConfig

from mro_equipment.models import Maintenance
from mro_contact.models import Department, Employee, Suplier
from mro_order.models import Order, OrderItem, OrderEmployee
from mro_order.tables import OrderTable

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
    objs = Order.objects.all()
    
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
    try:
        order = Order.objects.get(pk=order_id)
    except:
        order = Order()
    
    OrderInlineFormSet = inlineformset_factory(Order, OrderItem)
    if request.method == "POST":
        formset = OrderInlineFormSet(request.POST, request.FILES, instance=order)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect('/start/order/')
    else:
        formset = OrderInlineFormSet(instance=order)
    
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Work orders'),
        'lead': _('Edit and add work orders.'),
        'thumb': '/static/tango/48x48/status/awaiting-plus.png',
        'formset': formset,
    }
    response_dict['formset'] = formset
    
    return render(request, "formset.html", response_dict)

