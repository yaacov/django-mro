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
from django.db.models import Max
from django.template import Template, Context
from django.core.mail import EmailMessage
from django.template.loader import get_template

from django_tables2 import RequestConfig
from wkhtmltopdf.views import PDFTemplateView

from mro_system.models import Maintenance, System, Priority, Item, MaintenanceItem, Equipment
from mro_system.tables import EquipmentTable

from mro_contact.models import Department, Employee
from mro_order.models import Order, OrderItem, OrderDocument
from mro_order.tables import EquipmentTable, MaintenanceOrderTable
from mro_order.tables import MaintenanceTable, AllOrderTable, AssignTable, SimpleAssignTable
from mro_order.forms import OrderForm, SearchOrderForm, ActionOrderForm
from mro_order.forms import SimpleSearchOrderForm, SimpleActionOrderForm

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/order/',
    'image_url': '/static/tango/150x150/status/awaiting-plus.png',
    'name': ugettext_noop('Work Orders'),
    'description': ugettext_noop('Manage work orders, display and assigne maintenance work orders.'), 
}

# views
def order(request):
    '''
    '''
    
    thumbs = [
        {   'link': '/order/assign/',
            'image_url': '/static/tango/48x48/actions/add-participant.png',
            'name': ugettext_noop('Assing work orders to employees'),
            'description': ugettext_noop('Manage work orders, assigne work orders to employees.'), 
        }, 
        {
            'link': '/order/print/',
            'image_url': '/static/tango/48x48/actions/manage-students.png',
            'name': ugettext_noop('Print work orders for employees'),
            'description': _('Print work orders, print work orders assined to employees.'),
        },
        {
            'link': '/order/status/',
            'image_url': '/static/tango/48x48/actions/list-all-participants.png',
            'name': ugettext_noop('View work order status'),
            'description': _('View work orders, get status of work orders.'),
        },
        {
            'link': '/order/issue/',
            'image_url': '/static/tango/48x48/status/flag-red-clock.png',
            'name': ugettext_noop('Issue new work orders'),
            'description': ugettext_noop('Issue new work orders. Create and edit new maintenance work orders.'), 
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

# issue new work orders
# ---------------------

def issue(request, action = None, work_type = None):
    '''
    '''
    
    # get the employee data from the data base
    objs = Equipment.objects.all()
    
    # filter employees using the search form
    search = request.GET.get('search', '').strip()
    if search:
        objs &= Equipment.objects.filter(name__icontains = search)
#        objs |= System.objects.filter(serial_number__icontains = search)
        objs |= Equipment.objects.filter(description__icontains = search)
#        objs |= System.objects.filter(contract_number__icontains = search)
#        objs |= System.objects.filter(card_number__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= Equipment.objects.filter(department = filter_pk)
        filter_string = Department.objects.get(pk = filter_pk)
    
    if not filter_string:
        filter_string = _('Select department')
    
    # create a table object for the employee data
    table = EquipmentTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search
    response_dict['filters'] = Department.objects.all()
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string
    
    response_dict['table'] = table
    response_dict['add_action'] = True
    
    response_dict['headers'] = {
        'header': _('Issue new work orders'),
        'lead': _('Issue new work orders. Create and edit new maintenance work orders.'),
        'thumb': '/static/tango/48x48/status/flag-red-clock.png',
    }

    return render(request, 'mro_order/issue.html', response_dict)

def issue_order(request, equipment_pk = None, order_id = None, action = None):
    """
    """
    # get the employee data from the data base
    equipment = Equipment.objects.get(pk = equipment_pk)
    objs = Order.objects.filter(equipment = equipment).order_by('-created','-assigned','-completed')
   
    # filter employees using the search form
    search = request.GET.get('search', '').strip()
    if search:
        objs &= Order.objects.filter(assign_to__first_name__icontains = search)
        objs |= Order.objects.filter(assign_to__last_name__icontains = search)
        objs |= Order.objects.filter(equipment__name__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= Order.objects.filter(work_order_state = filter_pk)
        try:
            filter_string = dict(Order.ORDER_STATE)[filter_pk]
        except:
            filter_string = None
    
    if not filter_string:
        filter_string = _('Select work state')

    table = MaintenanceOrderTable(objs)

    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search
    response_dict['filters'] = Order.ORDER_STATE
    response_dict['current_filter_pk'] = filter_pk
    response_dict['current_filter_string'] = filter_string
    
    response_dict['table'] = table

    # get all maintenance instructions for this system
    maintenance = Maintenance.objects.filter(system = equipment.system)
    maintenance_table = MaintenanceTable(maintenance)
    response_dict['maintenance_table'] = maintenance_table

    response_dict['add_action'] = True

    response_dict['headers'] = {
        'thumb': '/static/tango/48x48/status/flag-red-clock.png',
        'header': _('Issue new work orders for: %(department)s - %(name)s') % {'name': equipment.name, 'department': equipment.department.name},
        'lead': _('Issue and edit new work orders for: %(department)s - %(name)s') % {'name': equipment.name, 'department': equipment.department.name},
    }

    return render(request, 'mro_order/issue_order.html', response_dict)

def manage_issue_order(request, equipment_pk = None, order_pk = None, maintenance_pk = None, next_url = None, update_url = None):
    '''
    '''

    if order_pk:
        order = Order.objects.get(pk = order_pk)
    else:
        order = None

    equipment = Equipment.objects.get(pk = equipment_pk)

    if not next_url:
        next_url = '/order/issue/%s/' % (equipment_pk)

    if request.method == "POST":
        ItemFormSet = inlineformset_factory(Order, OrderItem, extra = 1, can_delete = True)
        DocumentFormSet = inlineformset_factory(Order, OrderDocument, extra = 1, can_delete = True)

        orderform = OrderForm(request.POST, request.FILES, instance = order)
        itemformset = ItemFormSet(request.POST, request.FILES, instance = order, prefix='items')
        documentformset = DocumentFormSet(request.POST, request.FILES, instance = order, prefix='documents')
        
        action = request.POST['form-action']
        if action == '_delete':
            try:
                Order.objects.get(pk = order_pk).delete()
            except Exception, e:
                pass

            return HttpResponseRedirect(next_url)

        if orderform.is_valid() and itemformset.is_valid() and documentformset.is_valid():
            order = orderform.save()
            items = itemformset.save(commit=False)
            for item in items:
                item.order = order
                item.save()

            documents = documentformset.save(commit=False)
            for document in documents:

                document.order = order
                document.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if action == '_update':
                if not update_url:
                    update_url = '/order/issue/'

                return HttpResponseRedirect('%s%s' % (update_url, '%s/%s/' % (order.equipment.pk, order.pk)))

            return HttpResponseRedirect(next_url)
        else:
            messages.error(request, _('Error updating database.'))
    else:
        if order:
            initial = {}
            initial_items = []
        else:
            max_order = Order.objects.all().aggregate(Max('work_number'))
            if max_order['work_number__max']:
                work_number = max_order['work_number__max'] + 1
            else:
                work_number = 1

            if maintenance_pk:
                maintenance = Maintenance.objects.get(pk = maintenance_pk)

                initial = {
                    'work_number': work_number,
                    'maintenance': maintenance.pk,
                    'equipment': equipment,
                    'priority': maintenance.priority,
                    'work_description': maintenance.work_description,
                    #'assign_to': maintenance.assign_to,
#                    'contract_number': maintenance.system.contract_number,
#                    'contract_include_parts': maintenance.system.contract_include_parts,
#                    'assign_to': maintenance.system.assign_to,
                }

                initial_items = []
                for maintenanceitem in MaintenanceItem.objects.filter(maintenance = maintenance):
                    initial_items.append({
                        'work_number': work_number,
                        'item': maintenanceitem.item.pk,
                        'amount': maintenanceitem.amount,
                        'ordered': datetime.today(),
                    })
            else:
                initial = {
                    'work_number': work_number,
                    'equipment': equipment,
                    'priority': Priority.objects.all().order_by('-max_days_delay').first(),
#                    'contract_number': system.contract_number,
#                    'contract_include_parts': system.contract_include_parts,
                    'assign_to': equipment.assign_to,
                }
                initial_items = []

        ItemFormSet = inlineformset_factory(Order, OrderItem, extra = len(initial_items) + 1, can_delete = True)
        DocumentFormSet = inlineformset_factory(Order, OrderDocument, extra = 1, can_delete = True)

        orderform = OrderForm(instance = order, initial = initial)

        itemformset = ItemFormSet(instance = order, prefix='items')
        for subform, data in zip(itemformset.forms, initial_items):
            print subform.initial
            subform.initial = data
            print '===' , subform.initial

        documentformset = DocumentFormSet(instance = order, prefix='documents')

    response_dict = {}
    response_dict['headers'] = {
        'header': _('Work order for: %(department)s - %(name)s') % {'name': equipment.name, 'department': equipment.department.name},
        'lead': _('Edit work order for: %(department)s - %(name)s') % {'name': equipment.name, 'department': equipment.department.name},
        'thumb': '/static/tango/48x48/status/flag-red-clock.png',
    }
    response_dict['form'] = orderform
    response_dict['formset'] = itemformset
    response_dict['documentformset'] = documentformset

    return render(request, 'mro_order/manage_issue_order.html', response_dict)


# work order tables
# -----------------

def table(request):
    '''
    '''
    
    thumbs = [
        {
            'link': '/order/table/orders/',
            'image_url': '/static/tango/48x48/status/maintenance-time.png',
            'name': ugettext_noop('All work orders'),
            'description': _('Display all the work orders, search by wrok state, system and work description.'),
        },
    ]
    
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Work order reports'),
        'lead': _('Display work order Reports, search for order by wrok employee, system and work state.'),
        'thumb': '/static/tango/48x48/emblems/report-run.png',
    }
    
    response_dict['thumbs'] = thumbs
    
    return render(request, 'mro/base_list.html', response_dict)

def table_orders(request):
    """
    """
    # get the employee data from the data base
    objs = Order.objects.all().order_by('-created','-assigned','-completed')
    
    # filter employees using the search form
    search = request.GET.get('search', '').strip()
    if search:
        objs &= Order.objects.filter(assign_to__first_name__icontains = search)
        objs |= Order.objects.filter(assign_to__last_name__icontains = search)
        objs |= Order.objects.filter(system__name__icontains = search)
        objs |= Order.objects.filter(system__description__icontains = search)
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
        filter_string = _('Select work state')

    table = AllOrderTable(objs)

    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {
        'search': search,

        'filters': Order.ORDER_STATE,
        'current_filter_pk':filter_pk,
        'current_filter_string': filter_string,

        'table': table,
    }

    response_dict['table'] = table
    response_dict['headers'] = {
        'thumb': '/static/tango/48x48/status/maintenance-time.png',
        'header': _('All work orders'),
        'lead': _('Display all the work orders, search by wrok state, system and work description.'),
    }
    
    return render(request, 'mro_order/table_orders.html', response_dict)

def assign(request, simple_view = False):
    """
    """
    # get the employee data from the data base
    objs = Order.objects.all().order_by('-created','-assigned','-completed')
    
    department = None

    # filter employees using the search form
    search = request.GET.get('search', '').strip()
    if search:
        objs &= Order.objects.filter(assign_to__first_name__icontains = search)
        objs |= Order.objects.filter(assign_to__last_name__icontains = search)
        objs |= Order.objects.filter(equipment__name__icontains = search)
        objs |= Order.objects.filter(equipment__description__icontains = search)
        objs |= Order.objects.filter(maintenance__work_description__icontains = search)
        objs |= Order.objects.filter(work_description__icontains = search)
        objs |= Order.objects.filter(work_notes__icontains = search)

    if simple_view:
        searchform = SimpleSearchOrderForm(request.GET)
    else:
        searchform = SearchOrderForm(request.GET)

    if searchform.is_valid():
        if simple_view:
            work_order_state = 'RE'
            employee = ''
        else:
            work_order_state = searchform.cleaned_data['work_order_state'] or 'RE'
            employee = searchform.cleaned_data['employee']

        equipment = searchform.cleaned_data['equipment']
        
        if equipment.startswith('DE-'):
            

            department_pk = int(equipment[3:])
            department = Department.objects.filter(pk = department_pk)

            objs &= Order.objects.filter(equipment__department__pk = department_pk)

        if equipment.startswith('EQ-'):
            equipment_pk = int(equipment[3:])
            objs &= Order.objects.filter(equipment__pk = equipment_pk)

        if employee:
            objs &= Order.objects.filter(assign_to__pk = employee)

        if work_order_state not in ['AL',]:
            objs &= Order.objects.filter(work_order_state = work_order_state)
    else:
        # default is RE
        objs &= Order.objects.filter(work_order_state = 'RE')

    if simple_view:
        table = SimpleAssignTable(objs)
    else:
        table = AssignTable(objs)

    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    if request.method == "POST":
        if simple_view:
            actionfrom = SimpleActionOrderForm(request.POST)
        else:
            actionfrom = ActionOrderForm(request.POST)

        if actionfrom.is_valid():
            pks = request.POST.getlist("selection")
            selected_objects = Order.objects.filter(pk__in=pks)

            if simple_view:
                selected_action = 'AS'
            else:
                selected_action = actionfrom.cleaned_data['selected_action']
                
            if not selected_action or selected_action == 'AS':
                # assing to employee
                assign_to = actionfrom.cleaned_data['assign_to']
                if assign_to and selected_objects:
                    for order in selected_objects:
                        order.assign_to = Employee.objects.get(pk = assign_to)
                        order.work_order_state = 'AS'
                        order.save()

            if selected_action == 'CA':
                # cancel assing to employee
                if selected_objects:
                    for order in selected_objects:
                        order.assign_to = None
                        order.assigned = None
                        order.work_order_state = 'RE'
                        order.save()

            if selected_action == 'CW':
                # cancel work
                if selected_objects:
                    for order in selected_objects:
                        order.work_order_state = 'CA'
                        order.save()
            
            if selected_action == 'CO':
                # cancel work
                if selected_objects:
                    for order in selected_objects:
                        order.work_order_state = 'CO'
                        order.save()

    # base_table.html response_dict rendering information
    if simple_view:
        response_dict = {
            'search_form': SimpleSearchOrderForm(request.GET),
            'action_form': SimpleActionOrderForm(request.POST, department = department),
            'search': search,
            'table': table,
        }
    else:
        response_dict = {
            'search_form': SearchOrderForm(request.GET),
            'action_form': ActionOrderForm(request.POST),
            'search': search,
            'table': table,
        }

    response_dict['table'] = table
    response_dict['headers'] = {
        'thumb': '/static/tango/48x48/actions/add-participant.png',
        'header': _('Assing work orders to employees'),
        'lead': _('Manage work orders, assigne work orders to employees.'), 
        'simple_view': simple_view,
    }
    
    return render(request, 'mro_order/assign.html', response_dict)

def status(request, simple_view = False):
    """
    """
    # get the employee data from the data base
    objs = Order.objects.all().order_by('-created','-assigned','-completed')
    
    department = None

    # filter employees using the search form
    search = request.GET.get('search', '').strip()
    if search:
        objs &= Order.objects.filter(assign_to__first_name__icontains = search)
        objs |= Order.objects.filter(assign_to__last_name__icontains = search)
#        objs |= Order.objects.filter(system__name__icontains = search)
#        objs |= Order.objects.filter(system__description__icontains = search)
        objs |= Order.objects.filter(maintenance__work_description__icontains = search)
        objs |= Order.objects.filter(work_description__icontains = search)
        objs |= Order.objects.filter(work_notes__icontains = search)

    if simple_view:
        searchform = SimpleSearchOrderForm(request.GET)
    else:
        searchform = SearchOrderForm(request.GET)

    if searchform.is_valid():
        if simple_view:
            work_order_state = 'RE'
            employee = ''
        else:
            work_order_state = searchform.cleaned_data['work_order_state'] or 'RE'
            employee = searchform.cleaned_data['employee']

        equipment = searchform.cleaned_data['equipment']
        
        if equipment.startswith('DE-'):
            

            department_pk = int(equipment[3:])
            department = Department.objects.filter(pk = department_pk)

            objs &= Order.objects.filter(equipment__department__pk = department_pk)

        if equipment.startswith('EQ-'):
            equipment_pk = int(equipment[3:])
            objs &= Order.objects.filter(equipment__pk = equipment_pk)

        if employee:
            objs &= Order.objects.filter(assign_to__pk = employee)

        if work_order_state not in ['AL',]:
            objs &= Order.objects.filter(work_order_state = work_order_state)
    else:
        # default is RE
        objs &= Order.objects.filter(work_order_state = 'RE')

    if simple_view:
        table = SimpleAssignTable(objs)
    else:
        table = AssignTable(objs)

    RequestConfig(request, paginate={"per_page": 40}).configure(table)
    
    if request.method == "POST":
        if simple_view:
            actionfrom = SimpleActionOrderForm(request.POST)
        else:
            actionfrom = ActionOrderForm(request.POST)

        if actionfrom.is_valid():
            pks = request.POST.getlist("selection")
            selected_objects = Order.objects.filter(pk__in=pks)

            if simple_view:
                selected_action = 'AS'
            else:
                selected_action = actionfrom.cleaned_data['selected_action']
                
            if not selected_action or selected_action == 'AS':
                # assing to employee
                assign_to = actionfrom.cleaned_data['assign_to']
                if assign_to and selected_objects:
                    for order in selected_objects:
                        order.assign_to = Employee.objects.get(pk = assign_to)
                        order.work_order_state = 'AS'
                        order.save()

            if selected_action == 'CA':
                # cancel assing to employee
                if selected_objects:
                    for order in selected_objects:
                        order.assign_to = None
                        order.assigned = None
                        order.work_order_state = 'RE'
                        order.save()

            if selected_action == 'CW':
                # cancel work
                if selected_objects:
                    for order in selected_objects:
                        order.work_order_state = 'CA'
                        order.save()
            
            if selected_action == 'CO':
                # cancel work
                if selected_objects:
                    for order in selected_objects:
                        order.work_order_state = 'CO'
                        order.save()

    # base_table.html response_dict rendering information
    if simple_view:
        response_dict = {
            'search_form': SimpleSearchOrderForm(request.GET),
            'action_form': SimpleActionOrderForm(request.POST, department = department),
            'search': search,
            'table': table,
        }
    else:
        response_dict = {
            'search_form': SearchOrderForm(request.GET),
            'action_form': ActionOrderForm(request.POST),
            'search': search,
            'table': table,
        }
        
    response_dict['table'] = table
    response_dict['headers'] = {
        'thumb': '/static/tango/48x48/actions/list-all-participants.png',
        'header': _('View work order status'),
        'lead': _('View work orders, get status of work orders.'), 
        'simple_view': simple_view,
    }
    
    return render(request, 'mro_order/status.html', response_dict)

class PrintOrders(PDFTemplateView):

    def get(self, request, *args, **kwargs):
        self.response_class = self.html_response_class
        return super(PrintOrders, self).get(request,
            *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        post_print = request.POST.get("print", "")

        response_class = self.response_class
        try:
            if post_print != '_pdf' or request.GET.get('as', '') == 'html':
                # Use the html_response_class if HTML was requested.
                self.response_class = self.html_response_class
            return super(PrintOrders, self).get(request,
                *args, **kwargs)
        finally:
            # Remove self.response_class
            self.response_class = response_class

    def get_context_data(self, **kwargs):
        
        response_dict = super(PrintOrders, self).get_context_data(**kwargs)
        self.template_name = 'mro_order/print.html'
        request = self.request

        if request.method == "POST":
            pks = request.POST.getlist("selection")
            post_print = request.POST.get("print", "")
            orders = Order.objects.filter(pk__in=pks)
            self.template_name = 'mro_order/print_orders.html'
            
            response_dict['orders'] = orders
            response_dict['post_print'] = post_print
            
            if not orders:
                response_dict['post_print'] = ''
                self.response_class = self.html_response_class
                
            return response_dict
        
        # get the employee data from the data base
        objs = Order.objects.all().order_by('-created','-assigned','-completed')

        # filter employees using the search form
        search = request.GET.get('search', '').strip()
        if search:
            objs &= Order.objects.filter(assign_to__first_name__icontains = search)
            objs |= Order.objects.filter(assign_to__last_name__icontains = search)
            #objs |= Order.objects.filter(system__name__icontains = search)
            #objs |= Order.objects.filter(system__description__icontains = search)
            objs |= Order.objects.filter(maintenance__work_description__icontains = search)
            objs |= Order.objects.filter(work_description__icontains = search)
            objs |= Order.objects.filter(work_notes__icontains = search)

        searchform = SimpleSearchOrderForm(request.GET)
        #searchform = SearchOrderForm(request.GET)

        if searchform.is_valid():
            work_order_state = 'AS'
            employee = ''

            #work_order_state = searchform.cleaned_data['work_order_state'] or 'AS'
            employee = searchform.cleaned_data['employee']

            equipment = searchform.cleaned_data['equipment']

            if equipment.startswith('DE-'):
                department_pk = int(equipment[3:])
                objs &= Order.objects.filter(equipment__department__pk = department_pk)
            
            print objs

            if equipment.startswith('EQ-'):
                equipment_pk = int(equipment[3:])
                objs &= Order.objects.filter(equipment__pk = equipment_pk)
                
            print objs

            if employee:
                objs &= Order.objects.filter(assign_to__pk = employee)
                
            print objs

            if work_order_state not in ['AL',]:
                objs &= Order.objects.filter(work_order_state = work_order_state)
            
            print objs
        else:
            # default is AS
            objs &= Order.objects.filter(work_order_state = 'AS')
        
        print objs

        table = AssignTable(objs)
        RequestConfig(request, paginate={"per_page": 40}).configure(table)
        
        response_dict['search_form']=searchform
        response_dict['search']=search
        response_dict['table'] = table
        response_dict['headers'] = {
            'thumb': '/static/tango/48x48/actions/manage-students.png',
            'header': _('Print work orders for employees'),
            'lead': _('Print work orders, print work orders assined to employees.'),
        }

        return response_dict
