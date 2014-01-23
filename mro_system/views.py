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

from mro_system.models import System, Maintenance, Item, MaintenanceItem, SystemDocument
from mro_contact.models import Department, Employee

from mro_system.tables import SystemTable
from mro_system.tables import MaintenanceTable

from mro_system.forms import SystemForm, MaintenanceForm, SystemMaintenanceForm
from mro_system_type.models import SystemType,SystemTypeMaintenance

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/system/',
    'image_url': '/static/tango/150x150/actions/run.png',
    'name': ugettext_noop('Systems'),
    'description': ugettext_noop('Manage systems for maintenance, edit and add systems and equipment for maintenance.'), 
}

#    <select name="system_type" id="system-type-select">
#        <option value="0">{% trans 'New System' %}</option>
#        {% for t in system_types %}
#            <option value="{{t.id}}">{{t.name}}</option>
#        {% endfor %}
#    </select>

def system(request):
    '''
    '''
    
    # get the employee data from the data base
    objs = System.objects.all()
    system_types = SystemType.objects.all()
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= System.objects.filter(name__icontains = search)
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
    response_dict['system_types'] = system_types
    
    response_dict['headers'] = {
        'header': _('System list'),
        'lead': _('Manage systems for maintenance, edit and add systems and equipment for maintenance.'),
        'thumb': '/static/tango/48x48/actions/run.png',
    }
    
    return render(request, 'mro_system/base_table.html', response_dict)

def add_system_from_type(request):
    '''
    '''
    system_pk=request.GET.get('system_id', None)
    system_type_pk=request.GET.get('system_type_id', None)
    
    
    if system_type_pk!=None and system_type_pk!=0:
    
        try:
            systemtype = SystemType.objects.get(id=system_type_pk)
        except:
            return manage_system(request)
        
        systemtype_maintenance = SystemTypeMaintenance.objects.filter(system_type = systemtype)
        
        if system_pk == None:
            system = System()
            
            system.name = request.GET.get("name") or "%s System" % systemtype.name
            system.description = request.GET.get("description") or "A System that %s" % systemtype.description
#            if system.department:
            depart = request.GET.get("department") or None
            if depart:
              system.department = Department.objects.filter(id=depart).first()
            else:
              system.department = systemtype.department
            system.contract_include_parts = request.GET.get("contract_include_parts") or False
            system.location = request.GET.get("location") or ""
            system.contract_number = request.GET.get("contract_number") or ""
            
            assign_to = request.GET.get("department") or None
            if assign_to:
              system.assign_to = Employee.objects.filter(id=depart).first()
            
                        
            system.save()
        else:
            system = System.objects.get(id=system_pk)
        
        for maintenance in systemtype_maintenance:
            m = Maintenance()
            m.system = system
            m.work_cycle = maintenance.work_cycle
            m.work_cycle_count = maintenance.work_cycle_count
            
            m.save()
        
        #return manage_system(request,system_pk = system.id)
        return HttpResponseRedirect('/system/%s' % system.pk)
    else:
        return HttpResponseRedirect('/add/' )
    

def manage_system(request, system_pk = None):
    '''
    '''
    
    if system_pk == None:
        system = System()
    else:
        try:
            system = System.objects.get(id = system_pk)
        except:
            system = System()
            
    system_types = SystemType.objects.all()
    
    MaintenanceFormSet = inlineformset_factory(System, Maintenance, 
        extra = 1, can_delete=True, form=SystemMaintenanceForm)
    #DocumentFormSet = inlineformset_factory(System, SystemDocument, 
    #    extra = 1, can_delete = True)

    queryset = Maintenance.objects.filter(system = system) 

    search = request.GET.get('search', '')
    if search:
        queryset &= Maintenance.objects.filter(name__icontains = search)
        queryset |= Maintenance.objects.filter(work_description__icontains = search)

    paginator = Paginator(queryset, 10)
    page = request.GET.get('page', '')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    page_query = Maintenance.objects.filter(id__in=[object.pk for object in objects])

    if request.method == "POST":
        systemform = SystemForm(request.POST, instance=system)
        maintenanceformset = MaintenanceFormSet(request.POST, request.FILES, instance=system)
        #documentformset = DocumentFormSet(request.POST, request.FILES, instance = system, prefix='documents')

        if systemform.is_valid() and maintenanceformset.is_valid():
            system = systemform.save()
            maintenanceformset.save()

            #documents = documentformset.save(commit=False)
            #for document in documents:

            #    document.system = system
            #    document.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if '_continue' == request.POST.get('form-action', ''):
                return HttpResponseRedirect('/system/%s' % system.pk)

            return HttpResponseRedirect('/system/')
        else:
            messages.error(request, _('Error updating database.'))
    else:
        systemform = SystemForm(instance = system)
        maintenanceformset = MaintenanceFormSet(instance = system, queryset = page_query)
        #documentformset = DocumentFormSet(instance = system, prefix = 'documents')

    response_dict = {}
    response_dict['headers'] = {
        'header': _('System maintenance information'),
        'lead': _('Edit system information.'),
        'thumb': '/static/tango/48x48/actions/run.png',
    }
    response_dict['form'] = systemform
    response_dict['formset'] = maintenanceformset
    #response_dict['documentformset'] = documentformset
    response_dict['objects'] = objects
    response_dict['search'] = search
    response_dict['system_types'] = system_types
    response_dict['system_id'] = system.id

    return render(request, 'mro_system/manage_system.html', response_dict)

def manage_system_delete(request, system_pk = None):
    '''
    '''
    
    # try to get an system object
    try:
        system = System.objects.get(pk = system_pk)
        system.delete()
    except:
        pass
    
    return HttpResponseRedirect('/system/') # Redirect after POST

def manage_system_maintenance(request, system_pk = None, maintenance_pk = None):
    '''
    '''

    if maintenance_pk == None:
        maintenance = Maintenance()
    else:
        try:
            maintenance = Maintenance.objects.get(id = maintenance_pk)
        except:
            maintenance = Maintenance()

    ItemFormSet = inlineformset_factory(Maintenance, MaintenanceItem,
        extra = 1, can_delete=True, form=SystemMaintenanceForm)

    queryset = MaintenanceItem.objects.filter(maintenance = maintenance) 

    search = request.GET.get('search', '')
    if search:
        queryset &= MaintenanceItem.objects.filter(name__icontains = search)

    paginator = Paginator(queryset, 10)
    page = request.GET.get('page', '')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    page_query = MaintenanceItem.objects.filter(id__in=[object.pk for object in objects])

    if request.method == "POST":
        maintenanceform = MaintenanceForm(request.POST, instance=maintenance)
        itemformset = ItemFormSet(request.POST, request.FILES, instance=maintenance)
        
        if maintenanceform.is_valid() and itemformset.is_valid():
            maintenance = maintenanceform.save()
            itemformset.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if '_continue' == request.POST.get('form-action', ''):
                return HttpResponseRedirect('/system/%s/%s/' % (maintenance.system.pk, maintenance.pk))

            return HttpResponseRedirect('/system/%s/' % maintenance.system.pk)
        else:
            messages.error(request, _('Error updating database.'))
    else:
        maintenanceform = MaintenanceForm(instance=maintenance)
        itemformset = ItemFormSet(instance=maintenance, queryset=page_query)

    response_dict = {}
    response_dict['headers'] = {
        'header': _('Maintenanace instruction information, %(department)s') % {'department': maintenance.system.department.name},
        'lead': _('Edit maintenance instruction information for %(name)s - %(department)s') % {'name': maintenance.system.name, 'department': maintenance.system.department.name},

        'thumb': '/static/tango/48x48/status/flag-green-clock.png',
    }
    response_dict['form'] = maintenanceform
    response_dict['formset'] = itemformset
    response_dict['objects'] = objects
    response_dict['search'] = search

    return render(request, 'mro_system/manage_system_maintenance.html', response_dict)

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

