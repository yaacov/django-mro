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

from mro_theme.widgets import AdminImageWidget
from mro_contact.models import Employee, Department, Business

class EmployeeForm(ModelForm):
    ''' form for editing employee
    '''
    
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        
        self.helper.add_input(Submit('submit', _('Submit'), css_class='btn'))
        self.helper.add_input(Submit('delete', _('Delete'), css_class='btn-danger pull-right'))
        
        self.fields['image'].widget = AdminImageWidget()
        self.fields['address'].widget.attrs.update({'class' : 'wide'})
        self.fields['image'].widget.attrs.update({'class' : 'wide'})
        self.fields['email'].widget.attrs.update({'class' : 'ltr'})
        
    class Meta:
        model = Employee
        fields = ('last_name', 'first_name', 
            'phone', 'cell_phone', 'address', 
            'email', 'image', 'departments')

class BusinessForm(ModelForm):
    ''' form for editing business
    '''
    
    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        
        self.helper.add_input(Submit('submit', _('Submit'), css_class='btn'))
        self.helper.add_input(Submit('delete', _('Delete'), css_class='btn-danger pull-right'))
        
        self.fields['image'].widget = AdminImageWidget()
        self.fields['address'].widget.attrs.update({'class' : 'wide'})
        self.fields['image'].widget.attrs.update({'class' : 'wide'})
        self.fields['email'].widget.attrs.update({'class' : 'ltr'})
        
    class Meta:
        model = Business
        fields = ('name', 'contact_person', 
            'phone', 'fax', 'address', 
            'email', 'image', 'departments')
