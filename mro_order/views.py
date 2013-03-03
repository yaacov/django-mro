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

from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.shortcuts import render, render_to_response
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from django_tables2 import RequestConfig

from mro_system.models import Maintenance, System, Priority, Item, MaintenanceItem
from mro_contact.models import Department, Employee, Suplier
from mro_order.models import Order, OrderItem, OrderEmployee, OrderDocument
from mro_order.tables import OrderTable, SystemTable, MaintenanceOrderTable
from mro_order.tables import MaintenanceTable
from mro_order.forms import OrderForm, FractureOrderForm

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/order/',
    'image_url': '/static/tango/150x150/status/awaiting-plus.png',
    'name': ugettext_noop('Work Orders'),
    'description': ugettext_noop('Manage work orders, display and assigne maintenance work orders.'), 
}

# views
def work(request):
    '''
    '''
    
    thumbs = [
        {
            'link': '/order/fracture/',
            'image_url': '/static/tango/150x150/status/flag-red-clock.png',
            'name': ugettext_noop('Fracture work orders'),
            'description': ugettext_noop('Display and assigne fracture maintenance work orders.'), 
        },
        {   'link': '/order/maintenance/',
            'image_url': '/static/tango/150x150/status/flag-green-clock.png',
            'name': ugettext_noop('Maintenance work orders'),
            'description': ugettext_noop('Display and assigne maintenance work orders.'), 
        },
    ]
    
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Work orders'),
        'lead': _('Manage work orders, display and assigne maintenance work orders.'),
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
    
    objs &= Order.objects.filter(system__department = department_pk)
    #objs &= Order.objects.filter(work_type = ['MA', 'FR'][work_type == 'fracture'])
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        
        objs &= Order.objects.filter(assign_to__name__icontains = search)
        objs |= Order.objects.filter(system__name___icontains = search)
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
        {   'thumb': '/static/tango/48x48/status/flag-green-clock.png',
            'header': _('Maintenance'),
            'lead': _('Edit and create maintenance orders.'), 
        }, {
            'thumb': '/static/tango/48x48/status/flag-red-clock.png',
            'header': _('Fracture'),
            'lead': _('Edit and create fracture maintenance orders.'), 
        },
    ]
    response_dict['headers'] = thumbs[work_type == 'fracture']
    
    return render(request, 'mro/base_table.html', response_dict)

def manage_order(request, department_pk = None, order_id = None, action = None, work_type = 'fracture'):
    if  order_id == None:
        #order = Order(work_type = ['MA', 'FR'][work_type == 'fracture'])
        order = Order()
    else:
        try:
            order = Order.objects.get(id = order_id)
        except:
            order = Order(work_type = ['MA', 'FR'][work_type == 'fracture'])
            order = Order()

    ItemFormSet    = inlineformset_factory(Order, OrderItem, extra = 1, can_delete=True)
    queryset = OrderItem.objects.all() 

    EmployeeFormSet    = inlineformset_factory(Order, OrderEmployee, extra = 1, can_delete=True)
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
                    order.system.department.pk)
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
        'header': _('Maintenance order'),
        'lead': _('Edit maintenance order.'),
        'thumb': '/static/tango/48x48/actions/log-in.png',
    }
    response_dict['form'] = orderform
    response_dict['formset'] = itemformset
    response_dict['employeeformset'] = employeeformset

    return render(request, 'mro_order/manage_order_items.html', response_dict)

def system(request, action = None, work_type = None):
    '''
    '''
    
    # get the employee data from the data base
    objs = System.objects.all()
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= System.objects.filter(name__icontains = search)
        objs |= System.objects.filter(suplier__name__icontains = search)
        objs |= System.objects.filter(serial_number__icontains = search)
        objs |= System.objects.filter(description__icontains = search)
        objs |= System.objects.filter(contract_number__icontains = search)
        objs |= System.objects.filter(card_number__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= System.objects.filter(department = filter_pk)
        filter_string = Department.objects.get(pk = filter_pk)
    
    if not filter_string:
        filter_string = _('All')
    
    # create a table object for the employee data
    table = SystemTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search
    response_dict['filters'] = Department.objects.all()
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string
    
    response_dict['table'] = table
    response_dict['add_action'] = True
    
    thumbs = [
        {   'header': _('Maintenance work orders'),
            'lead': _('Display and assigne maintenance work orders.'),
            'thumb': '/static/tango/48x48/status/flag-green-clock.png',
        }, {
            'header': _('Fracture work orders'),
            'lead': _('Display and assigne fracture maintenance work orders.'),
            'thumb': '/static/tango/48x48/status/flag-red-clock.png',
        },
    ]
    response_dict['headers'] = thumbs[work_type == 'fracture']

    return render(request, 'mro_order/system.html', response_dict)

def system_order(request, system_pk = None, order_id = None, action = None, work_type = 'fracture'):
    """
    """
    # get the employee data from the data base
    system = System.objects.get(pk = system_pk)
    objs = Order.objects.filter(system = system).order_by('-created','-assigned','-completed')
   
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= Order.objects.filter(assign_to__first_name__icontains = search)
        objs |= Order.objects.filter(assign_to__last_name__icontains = search)
        objs |= Order.objects.filter(system__name__icontains = search)
    
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

    if work_type == 'fracture':
        objs &= Order.objects.filter(maintenance__isnull = True)
        table = OrderTable(objs)
    else:
        objs &= Order.objects.filter(maintenance__isnull = False)
        table = MaintenanceOrderTable(objs)

    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search
    response_dict['filters'] = Order.ORDER_STATE
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string
    
    response_dict['table'] = table

    if work_type == 'maintenance':
        # get all maintenance instructions for this system
        maintenance = Maintenance.objects.filter(system = system)
        maintenance_table = MaintenanceTable(maintenance)
        response_dict['maintenance_table'] = maintenance_table

    response_dict['add_action'] = True
    
    thumbs = [
        {   'thumb': '/static/tango/48x48/status/flag-green-clock.png',
            'header': _('Maintenance work orders, %(department)s') % {'department': system.department.name},
            'lead': _('Edit and issue maintenance work orders for %(name)s - %(department)s') % {'name': system.name, 'department': system.department.name},
        }, {
            'thumb': '/static/tango/48x48/status/flag-red-clock.png',
            'header': _('Fracture work orders, %(department)s') % {'department': system.department.name},
            'lead': _('Edit and issue fracture work orders for %(name)s - %(department)s') % {'name': system.name, 'department': system.department.name},
        },
    ]
    response_dict['headers'] = thumbs[work_type == 'fracture']
    
    if work_type == 'fracture':
        return render(request, 'mro_order/system_fracture_order.html', response_dict)
    else:
        return render(request, 'mro_order/system_maintenance_order.html', response_dict)

def manage_fracture_order(request, system_pk = None, order_pk = None, action = None, work_type = 'fracture'):
    '''
    '''

    if order_pk:
        order = Order.objects.get(pk = order_pk)
    else:
        order = None

    if request.method == "POST":
        ItemFormSet = inlineformset_factory(Order, OrderItem, extra = 1, can_delete = True)
        EmployeeFormSet = inlineformset_factory(Order, OrderEmployee, extra = 1, can_delete = True)
        DocumentFormSet = inlineformset_factory(Order, OrderDocument, extra = 1, can_delete = True)

        orderform = OrderForm(request.POST, request.FILES, instance = order)
        itemformset = ItemFormSet(request.POST, request.FILES, instance = order, prefix='items')
        employeeformset = EmployeeFormSet(request.POST, request.FILES, instance = order, prefix='employees')
        documentformset = DocumentFormSet(request.POST, request.FILES, instance = order, prefix='documents')
        
        action = request.POST['form-action']
        if action == '_delete':
            try:
                Order.objects.get(pk = order_pk).delete()
            except Exception, e:
                pass

            return HttpResponseRedirect('/order/fracture/%s/' % (system_pk))

        if orderform.is_valid() and itemformset.is_valid() and employeeformset.is_valid() and documentformset.is_valid():
            order = orderform.save()
            items = itemformset.save(commit=False)
            for item in items:
                item.order = order
                item.save()

            employees = employeeformset.save(commit=False)
            for employee in employees:
                employee.order = order
                employee.save()

            documents = documentformset.save(commit=False)
            for document in documents:

                document.order = order
                document.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if action == '_update':
                return HttpResponseRedirect('/order/fracture/%s/%s/' % (system_pk, order.pk))

            return HttpResponseRedirect('/order/fracture/%s/' % (system_pk))
        else:
            messages.error(request, _('Error updating database.'))
    else:
        ItemFormSet = inlineformset_factory(Order, OrderItem, extra = 1, can_delete = True)
        EmployeeFormSet = inlineformset_factory(Order, OrderEmployee, extra = 1, can_delete = True)
        DocumentFormSet = inlineformset_factory(Order, OrderDocument, extra = 1, can_delete = True)

        system = System.objects.get(pk = system_pk)

        initial = {
            'system': system,
            'priority': Priority.objects.all().order_by('-max_days_delay')[0],
            'contract_number': system.contract_number,
            'contract_include_parts': system.contract_include_parts,
            'assign_to_suplier': system.suplier,
        }

        orderform = OrderForm(instance = order, initial = initial)
        employeeformset = EmployeeFormSet(instance = order, prefix='employees')
        itemformset = ItemFormSet(instance = order, prefix='items')
        documentformset = DocumentFormSet(instance = order, prefix='documents')

    system = System.objects.get(pk = system_pk)
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Fracture work order, %(department)s') % {'department': system.department.name},
        'lead': _('Edit fracture work order for %(name)s - %(department)s') % {'name': system.name, 'department': system.department.name},
        'thumb': '/static/tango/48x48/status/flag-red-clock.png',
    }
    response_dict['form'] = orderform
    response_dict['formset'] = itemformset
    response_dict['employeeformset'] = employeeformset
    response_dict['documentformset'] = documentformset

    return render(request, 'mro_order/manage_order_items.html', response_dict)

def manage_maintenance_order(request, system_pk = None, order_pk = None, maintenance_pk = None, action = None, work_type = 'maintenance'):
    '''
    '''

    if order_pk:
        order = Order.objects.get(pk = order_pk)
    else:
        order = None

    if request.method == "POST":
        ItemFormSet = inlineformset_factory(Order, OrderItem, extra = 1, can_delete = True)
        EmployeeFormSet = inlineformset_factory(Order, OrderEmployee, extra = 1, can_delete = True)
        DocumentFormSet = inlineformset_factory(Order, OrderDocument, extra = 1, can_delete = True)

        orderform = OrderForm(request.POST, request.FILES, instance = order)
        itemformset = ItemFormSet(request.POST, request.FILES, instance = order, prefix='items')
        employeeformset = EmployeeFormSet(request.POST, request.FILES, instance = order, prefix='employees')
        documentformset = DocumentFormSet(request.POST, request.FILES, instance = order, prefix='documents')
        
        action = request.POST['form-action']
        if action == '_delete':
            try:
                Order.objects.get(pk = order_pk).delete()
            except Exception, e:
                pass

            return HttpResponseRedirect('/order/maintenance/%s/' % (system_pk))

        if orderform.is_valid() and itemformset.is_valid() and employeeformset.is_valid() and documentformset.is_valid():
            order = orderform.save()
            items = itemformset.save(commit=False)
            for item in items:
                item.order = order
                item.save()

            employees = employeeformset.save(commit=False)
            for employee in employees:
                employee.order = order
                employee.save()

            documents = documentformset.save(commit=False)
            for document in documents:

                document.order = order
                document.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if action == '_update':
                return HttpResponseRedirect('/order/maintenance/%s/%s/' % (system_pk, order.pk))

            return HttpResponseRedirect('/order/maintenance/%s/' % (system_pk))
        else:
            messages.error(request, _('Error updating database.'))
    else:
        if order:
            initial = {}
            initial_items = []
        else:
            # if we have a maintenace object
            if maintenance_pk:
                maintenance = Maintenance.objects.get(pk = maintenance_pk)

                initial = {
                    'maintenance': maintenance.pk,
                    'system': maintenance.system,
                    'priority': maintenance.priority,
                    'work_description': maintenance.work_description,
                    #'assign_to': maintenance.assign_to,
                    'estimated_work_time': maintenance.estimated_work_time,
                    'contract_number': maintenance.system.contract_number,
                    'contract_include_parts': maintenance.system.contract_include_parts,
                    'assign_to_suplier': maintenance.system.suplier,
                }

                initial_items = []
                for maintenanceitem in MaintenanceItem.objects.filter(maintenance = maintenance):
                    initial_items.append({
                        'item': maintenanceitem.item.pk,
                        'amount': maintenanceitem.amount,
                        'ordered': datetime.today(),
                        })

        ItemFormSet = inlineformset_factory(Order, OrderItem, extra = len(initial_items) + 1, can_delete = True)
        EmployeeFormSet = inlineformset_factory(Order, OrderEmployee, extra = 1, can_delete = True)
        DocumentFormSet = inlineformset_factory(Order, OrderDocument, extra = 1, can_delete = True)

        orderform = OrderForm(instance = order, initial = initial)
        employeeformset = EmployeeFormSet(instance = order, prefix='employees')

        itemformset = ItemFormSet(instance = order, prefix='items')
        for subform, data in zip(itemformset.forms, initial_items):
            print subform.initial
            subform.initial = data
            print '===' , subform.initial

        documentformset = DocumentFormSet(instance = order, prefix='documents')

    system = System.objects.get(pk = system_pk)
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Maintenanace work order, %(department)s') % {'department': system.department.name},
        'lead': _('Edit maintenance work order for %(name)s - %(department)s') % {'name': system.name, 'department': system.department.name},
        'thumb': '/static/tango/48x48/status/flag-green-clock.png',
    }
    response_dict['form'] = orderform
    response_dict['formset'] = itemformset
    response_dict['employeeformset'] = employeeformset
    response_dict['documentformset'] = documentformset

    return render(request, 'mro_order/manage_order_items.html', response_dict)
