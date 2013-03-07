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

from mro_order.models import Order
from mro_contact.models import Employee, Suplier

class FractureOrderForm(ModelForm):
    can_delete = True

    def __init__(self, *args, **kwargs):
        super(FractureOrderForm, self).__init__(*args, **kwargs)

        # if we have an item, we can set the amount unit widget,
        # on items we do not know, we do not set the amount unit widget
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            pass
            #self.fields['assign_to'].queryset = Employee.objects.filter(departments = instance.system.department).only('id', 'first_name', 'last_name')
            #self.fields['assign_to_suplier'].queryset = Suplier.objects.filter(departments = instance.system.department).only('id', 'name')

    class Meta:
        model = Order
        fields = ('work_description', 'work_notes',
            'estimated_work_time', 'priority', 
            'contract_number', 'contract_include_parts', 
            'assign_to', 
            'work_order_state', 'estimated_completion', 'created', 'assigned', 'completed',)

class OrderForm(ModelForm):
    can_delete = True

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['system'].widget = forms.HiddenInput()
        self.fields['maintenance'].widget = forms.HiddenInput()

        # if we have an item, we can set the amount unit widget,
        # on items we do not know, we do not set the amount unit widget
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            pass
            #self.fields['assign_to'].queryset = Employee.objects.filter(departments = instance.system.department).only('id', 'first_name', 'last_name')
            #self.fields['assign_to_suplier'].queryset = Suplier.objects.filter(departments = instance.system.department).only('id', 'name')

    class Meta:
        model = Order
        fields = ('system', 'maintenance', 'work_description', 'work_notes',
            'estimated_work_time', 'priority', 
            'contract_number', 'contract_include_parts', 
            'assign_to', 
            'work_order_state', 'estimated_completion', 'created', 'assigned', 'completed',)
