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

from mro_warehouse.models import Item, Warehouse, WarehouseItem
from mro_warehouse.forms import WarehouseForm, WarehouseItemForm

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/warehouse/',
    'image_url': '/static/tango/150x150/actions/arrange-boxes.png',
    'name': ugettext_noop('Warehouse'),
    'description': ugettext_noop('Manage warehouse and items. Issue and insert items to and from warehouse storage.'), 
}

# views
def warehouse(request):
    '''
    '''
    
    response_dict = {
        'headers': {
            'header': _('Warehouse'),
            'lead': _('Manage warehouse and items. Issue and insert items to and from warehouse storage.'),
            'thumb': '/static/tango/48x48/actions/arrange-boxes.png',
        },
        'thumbs': [ 
            {
                'link': '/warehouse/warehouse_items/',
                'image_url': '/static/tango/150x150/actions/log-in.png',
                'name': ugettext_noop('Warehouse Items'),
                'description': ugettext_noop('Manage items in warehouse. Issue and insert items to and from the warehouse.'), 
            },
            {   'link': '/warehouse/items/',
                'image_url': '/static/tango/150x150/emblems/function.png',
                'name': ugettext_noop('Item information'),
                'description': ugettext_noop('Manage items. Edit and add item information.'), 
            },
        ],
    }

    return render(request, 'mro_warehouse/base_list.html', response_dict)

def manage_items(request):
    '''
    '''

    ItemFormSet = modelformset_factory(Item, 
        fields=('name', 'catalogic_number', 'unit', 'description'),
        can_delete=True)
    queryset = Item.objects.all() 

    search = request.GET.get('search', '')
    if search:
        queryset &= Item.objects.filter(name__icontains = search)
        queryset |= Item.objects.filter(catalogic_number__icontains = search)

    paginator = Paginator(queryset, 45)
    page = request.GET.get('page', '')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    page_query = Item.objects.filter(id__in=[object.id for object in objects])
    formset = ItemFormSet(queryset = page_query)
    if request.method == 'POST':
        formset = ItemFormSet(request.POST)

        if formset.is_valid():
            formset.save()

            messages.success(request, _('Database updated.'))

            return HttpResponseRedirect('/warehouse/items/')
        else:
            messages.error(request, _('Error updating database.'))
            
    response_dict = {}
    response_dict['headers'] = {
        'header': _('Items'),
        'lead': _('Manage items. Edit and add item information.'),
        'thumb': '/static/tango/48x48/emblems/function.png',
    }
    response_dict['formset'] = formset
    response_dict['objects'] = objects
    response_dict['search'] = search

    return render(request, 'mro_warehouse/manage_items.html', response_dict)

def manage_warehouse_items(request, warehouse_id = 1):
    '''
    '''
    
    if  warehouse_id == None:
        warehouse = Warehouse()
    else:
        try:
            warehouse = Warehouse.objects.get(id = warehouse_id)
        except:
            warehouse = Warehouse()

    ItemFormSet    = inlineformset_factory(Warehouse, WarehouseItem, 
        extra = 1, can_delete=True, form=WarehouseItemForm)

    queryset = WarehouseItem.objects.all() 

    search = request.GET.get('search', '')
    if search:
        queryset &= WarehouseItem.objects.filter(item__name__icontains = search)
        queryset |= WarehouseItem.objects.filter(item__catalogic_number__icontains = search)

    expires = request.GET.get('expires', '')
    if expires:
        try:
            y, m, d = map(int, expires.split('-'))
            queryset &= WarehouseItem.objects.filter(expires__lt = date(y, m, d))
        except:
            messages.warning(request, _('Warning, bad date format.'))
            expires = ''

    amount = request.GET.get('amount', '')
    if amount:
        try:
            if amount.startswith('>'):
                amount_gt = amount[1:]
                queryset &= WarehouseItem.objects.filter(amount__gt = int(amount_gt))
            else:
                queryset &= WarehouseItem.objects.filter(amount__lt = int(amount))
        except:
            messages.warning(request, _('Warning, bad amount.'))
            amount = ''

    paginator = Paginator(queryset, 45)
    page = request.GET.get('page', '')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    page_query = WarehouseItem.objects.filter(id__in=[object.id for object in objects])

    if request.method == "POST":
        warehouseform = WarehouseForm(request.POST, instance=warehouse)
        itemformset = ItemFormSet(request.POST, request.FILES, instance=warehouse)
        
        if warehouseform.is_valid() and itemformset.is_valid():
            warehouseform.save()
            itemformset.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if '_save' in request.POST:
                return HttpResponseRedirect('/warehouse/warehouse_items/')
            if '_addanother' in request.POST:
                return HttpResponseRedirect('/warehouse/warehouse_items/')

            return HttpResponseRedirect('/warehouse/warehouse_items/')
        else:
            messages.error(request, _('Error updating database.'))
    else:
        warehouseform = WarehouseForm(instance=warehouse)
        itemformset = ItemFormSet(instance=warehouse, queryset=page_query)

    response_dict = {}
    response_dict['headers'] = {
        'header': _('Warehouse Items'),
        'lead': _('Manage items in warehouse. Issue and insert items to and from the warehouse.'),
        'thumb': '/static/tango/48x48/actions/log-in.png',
    }
    response_dict['form'] = warehouseform
    response_dict['formset'] = itemformset
    response_dict['objects'] = objects
    response_dict['search'] = search
    response_dict['expires'] = expires
    response_dict['amount'] = amount

    return render(request, 'mro_warehouse/manage_warehouse_items.html', response_dict)
