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

from mro_contract.models import Contract, ContractDocument

from mro_contract.tables import ContractTable
from mro_contract.forms import ContractForm

# a thumbnail button to show in the projects start page
thumb = {
    'link': '/contract/',
    'image_url': '/static/tango/150x150/categories/bookmark.png',
    'name': ugettext_noop('Contracts'),
    'description': ugettext_noop('Manage contract for maintenance, edit and add systems and contract for maintenance.'), 
}

def contract(request):
    '''
    '''
    
    # get the employee data from the data base
    objs = Contract.objects.all()
    
    # filter employees using the search form
    search = request.GET.get('search', '')
    if search:
        objs &= Contract.objects.filter(number__icontains = search)
        objs |= Contract.objects.filter(description__icontains = search)
        objs |= Contract.objects.filter(business__name__icontains = search)
    
    # create a table object for the employee data
    table = ContractTable(objs)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    
    # base_table.html response_dict rendering information
    response_dict = {}
    response_dict['search'] = search
    response_dict['filters'] = None
    
    response_dict['table'] = table
    response_dict['add_action'] = True
    
    response_dict['headers'] = {
        'header': _('Contract list'),
        'lead': _('Manage contracts for maintenance, edit and add contracts for maintenance.'),
        'thumb': '/static/tango/48x48/categories/bookmark.png',
    }
    
    return render(request, 'mro_contract/base_table.html', response_dict)

def manage_contract(request, contract_pk = None):
    '''
    '''
    
    if contract_pk == None:
        contract = Contract()
    else:
        try:
            contract = Contract.objects.get(id = contract_pk)
        except:
            contract = Contract()

    DocumentFormSet = inlineformset_factory(Contract, ContractDocument, 
        extra = 1, can_delete = True)

    if request.method == "POST":
        contractform = ContractForm(request.POST, instance = contract)
        documentformset = DocumentFormSet(request.POST, request.FILES, instance = contract, prefix='documents')

        if contractform.is_valid() and documentformset.is_valid():
            contract = contractform.save()

            documents = documentformset.save(commit = False)
            for document in documents:

                document.contract = contract
                document.save()

            messages.success(request, _('Database updated.'))

            # Redirect to somewhere
            if '_continue' == request.POST.get('form-action', ''):
                return HttpResponseRedirect('/contract/%s' % contract.pk)

            return HttpResponseRedirect('/contract/')
        else:
            messages.error(request, _('Error updating database.'))
    else:
        contractform = ContractForm(instance = contract)
        documentformset = DocumentFormSet(instance = contract, prefix = 'documents')

    response_dict = {}
    response_dict['headers'] = {
        'header': _('Contract'),
        'lead': _('Edit Contract information.'),
        'thumb': '/static/tango/48x48/categories/bookmark.png',
    }
    response_dict['form'] = contractform
    response_dict['documentformset'] = documentformset

    return render(request, 'mro_contract/manage_contract.html', response_dict)

def manage_contract_delete(request, contract_pk = None):
    '''
    '''
    
    # try to get an system object
    try:
        contract = Contract.objects.get(pk = contract_pk)
        contract.delete()
    except:
        pass
    
    return HttpResponseRedirect('/contract/') # Redirect after POST
