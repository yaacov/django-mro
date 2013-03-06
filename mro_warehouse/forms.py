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

from django.forms import ModelForm, TextInput, CharField

from mro_theme.widgets import AmountWidget
from mro_warehouse.models import Item, Warehouse, WarehouseItem, WarehouseLog

class WarehouseForm(ModelForm):
    can_delete = True

    class Meta:
        model = Warehouse
        fields = ('name',)

class WarehouseItemForm(ModelForm):
    can_delete = True

    def clean_item(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.item
        else:
            return self.cleaned_data.get('item', None)
            
    def __init__(self, *args, **kwargs):
        super(WarehouseItemForm, self).__init__(*args, **kwargs)

        # if we have an item, we can set the amount unit widget,
        # on items we do not know, we do not set the amount unit widget
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            # set the widget to be amount widget
            self.fields['amount'].widget = AmountWidget({
                'unit': instance.item.unit_str(),
            })
            
            # make the item widget none seateble
            self.fields['item'].required = False
            self.fields['item'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = WarehouseItem

class WarehouseLogForm(ModelForm):

    class Meta:
        model = WarehouseLog

        fields = (
            'item', 'action', 'amount',
            'shelve', 'batch', 'expires',)
