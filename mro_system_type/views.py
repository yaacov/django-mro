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

from mro_system_type.models import SystemType, SystemTypeMaintenance
from mro_contact.models import Department

from django_tables2   import RequestConfig

from mro_system_type.tables import SystemTypeTable
from mro_system_type.tables import SystemTypeMaintenanceTable

from mro_system_type.forms import SystemTypeForm, SystemTypeSystemMaintenanceForm, SystemTypeMaintenanceForm

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/systemtype/',
    'image_url': '/static/tango/150x150/actions/load-settings.png',
    'name': ugettext_noop('System Types'),
    'description': ugettext_noop('Manage system typess for maintenance.'), 
}

def system_type(request):
    '''
    '''
    
    # get the employee data from the data base
    objs = SystemType.objects.all()
    search = request.GET.get('search', '')
    if search:
        objs &= SystemType.objects.filter(name__icontains = search)
        objs |= SystemType.objects.filter(description__icontains = search)
    
    filter_pk = request.GET.get('filter_pk', '')
    filter_string = None
    if filter_pk:
        objs &= SystemType.objects.filter(department = filter_pk)
        filter_string = Department.objects.get(pk = filter_pk)
        
    if not filter_string:
        filter_string = _('All')
        
    # create a table object for the employee data
    table = SystemTypeTable(objs)
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
        'header': _('System Types list'),
        'lead': _('Manage system types for maintenance.'),
        'thumb': '/static/tango/48x48/actions/run.png',
    }
    
    return render(request, 'mro_system_type/base_table.html', response_dict)
    
def manage_system_type(request, system_type_pk = None):
    '''
    '''
    
    if system_type_pk == None:
        systemtype = SystemType()
    else:
        try:
            systemtype = SystemType.objects.get(id = system_type_pk)
        except:
            systemtype = SystemType()

    MaintenanceFormSet = inlineformset_factory(SystemType, SystemTypeMaintenance, 
        extra = 1, can_delete=True, form=SystemTypeSystemMaintenanceForm)
    #DocumentFormSet = inlineformset_factory(System, SystemDocument, 
    #    extra = 1, can_delete = True)

    queryset = SystemTypeMaintenance.objects.filter(system_type = systemtype) 

    search = request.GET.get('search', '')
    if search:
        queryset &= SystemTypeMaintenance.objects.filter(name__icontains = search)
        queryset |= SystemTypeMaintenance.objects.filter(work_description__icontains = search)

    paginator = Paginator(queryset, 10)
    page = request.GET.get('page', '')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    page_query = SystemTypeMaintenance.objects.filter(id__in=[object.pk for object in objects])

    if request.method == "POST":
        systemtypeform = SystemTypeForm(request.POST, instance=systemtype)
        systemtype_maintenanceformset = MaintenanceFormSet(request.POST, request.FILES, instance=systemtype)
        #documentformset = DocumentFormSet(request.POST, request.FILES, instance = system, prefix='documents')

        if systemtypeform.is_valid() and systemtype_maintenanceformset.is_valid():
            systemtype = systemtypeform.save()
            systemtype_maintenanceformset.save()

            #documents = documentformset.save(commit=False)
            #for document in documents:

            #    document.system = system
            #    document.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if '_continue' == request.POST.get('form-action', ''):
                return HttpResponseRedirect('/systemtype/%s' % systemtype.pk)

            return HttpResponseRedirect('/systemtype/')
        else:
            messages.error(request, _('Error updating database.'))
    else:
        systemtype_form = SystemTypeForm(instance = systemtype)
        maintenanceformset = MaintenanceFormSet(instance = systemtype, queryset = page_query)
        #documentformset = DocumentFormSet(instance = system, prefix = 'documents')

    response_dict = {}
    response_dict['headers'] = {
        'header': _('System maintenance information'),
        'lead': _('Edit system information.'),
        'thumb': '/static/tango/48x48/actions/run.png',
    }
    response_dict['form'] = systemtype_form
    response_dict['formset'] = maintenanceformset
    #response_dict['documentformset'] = documentformset
    response_dict['objects'] = objects
    response_dict['search'] = search

    return render(request, 'mro_system_type/manage_system.html', response_dict)

def manage_system_type_delete(request, system_type_pk = None):
    '''
    '''
    
    # try to get an system object
    try:
        systemtype = SystemType.objects.get(pk = system_type_pk)
        systemtype.delete()
    except:
        pass
    
    return HttpResponseRedirect('/systemtype/') # Redirect after POST

def manage_system_type_maintenance(request, system_type_pk = None, maintenance_type_pk = None):
    '''
    '''

    if maintenance_type_pk == None:
        maintenance = SystemTypeMaintenance()
    else:
        try:
            maintenance = SystemTypeMaintenance.objects.get(id = maintenance_type_pk)
        except:
            maintenance = SystemTypeMaintenance()

    if request.method == "POST":
        maintenanceform = MaintenanceForm(request.POST, instance=maintenance)
        
        if maintenanceform.is_valid():
            maintenance = maintenanceform.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if '_continue' == request.POST.get('form-action', ''):
                return HttpResponseRedirect('/systemtype/%s/%s/' % (maintenance.system_type.pk, maintenance.pk))

            return HttpResponseRedirect('/systemtype/%s/' % maintenance.system_type.pk)
        else:
            messages.error(request, _('Error updating database.'))
    else:
        maintenanceform = SystemTypeMaintenanceForm(instance=maintenance)

    response_dict = {}
    response_dict['headers'] = {
        'header': _('Maintenanace instruction information, %(department)s') % {'department': maintenance.system_type.department.name},
        'lead': _('Edit maintenance instruction information for %(name)s - %(department)s') % {'name': maintenance.system_type.name, 'department': maintenance.system_type.department.name},

        'thumb': '/static/tango/48x48/status/flag-green-clock.png',
    }
    response_dict['form'] = maintenanceform

    return render(request, 'mro_system_type/manage_system_maintenance.html', response_dict)

def run_cron(request):
    '''
    '''
    pass
