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
# Author: Yaacov Zamir (2013) <kobi.zamir@gmail.com>

from django import forms

from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiField, Fieldset, ButtonHolder
from crispy_forms.layout import Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from mro_theme.widgets import AdminImageWidget
from mro_system.models import System, Maintenance
from mro_warehouse.models import Item, Warehouse, WarehouseItem

class SystemForm(ModelForm):
    ''' form for editing employee
    '''
    
    def __init__(self, *args, **kwargs):
        super(SystemForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        
        self.fields['image'].widget = AdminImageWidget()
        #self.fields['address'].widget.attrs.update({'class' : 'wide'})
        self.fields['description'].widget.attrs.update({'class': 'wide', 'rows': '6'})
        
    class Meta:
        model = System
        fields = ('name', 
            'serial_number', 
            'card_number', 
            'contract_number',
            'contract_include_parts',
            'suplier','department', 
            'image', 'description',)

class SystemMaintenanceForm(ModelForm):
    '''
    '''

    can_delete = True

    class Meta:
        model = Maintenance
        exclude = ('items', 'priority', 'assign_to', 'counter_command')

class MaintenanceForm(ModelForm):
    ''' form for editing MaintenanceInstructionForm
    '''
    
    def __init__(self, *args, **kwargs):
        super(MaintenanceForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        
        self.helper.add_input(Submit('submit', _('Submit'), css_class='btn'))
        #self.helper.add_input(Submit('update', _('Update'), css_class='btn-success'))
        self.helper.add_input(Submit('delete', _('Delete'), css_class='btn-danger pull-right'))
        
        self.fields['work_description'].widget.attrs.update({'class' : 'wide', 'rows': '6'})
        
    class Meta:
        model = Maintenance
        exclude = ('items', 'priority', 'assign_to',)
        
