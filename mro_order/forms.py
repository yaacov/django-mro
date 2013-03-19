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

from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiField, Fieldset, ButtonHolder
from crispy_forms.layout import Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from django.forms import ModelForm

from mro_order.models import Order
from mro_contact.models import Employee, Department
from mro_system.models import Maintenance, System, Priority, Item, MaintenanceItem

class OrderForm(ModelForm):
    can_delete = True

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['system'].widget = forms.HiddenInput()
        self.fields['maintenance'].widget = forms.HiddenInput()

    class Meta:
        model = Order
        fields = ('work_number', 
            'system', 'maintenance', 
            'work_description', 'work_notes',
            'work_time',
            'priority', 
            'contract_number', 'contract_include_parts', 
            'assign_to', 
            'work_order_state', 
            'created', 
            'assigned', 
            'completed',
            'work_started_time',
            'work_end_time',)

class SearchOrderForm(forms.Form):
    system = forms.ChoiceField(label=_("Department and System"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    employee = forms.ChoiceField(label=_("Employee"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    #work_order_state = forms.ChoiceField(label=_("Work state"), required = False, choices=(),
    #    widget=forms.Select(attrs={'class':'selector'}))

    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)

        choices = [
            ('', _('Select department')),
        ]
        choices += [('DE-%d' % pt.id, '%s: %s' % (_('Department'), pt)) for pt in Department.objects.all()]
        choices += [('SY-%d' % pt.id, '%s: %s' % (_('System'), pt)) for pt in System.objects.all()]
        self.fields['system'].choices = choices

        instance = getattr(self, 'instance', None)
        choices = [
            ('', _('Select employee')),
        ]
        
        if 'system' in self.data:
            choices += [(u'%d' % pt.id, u'%s' % (pt)) for pt in Employee.objects.filter(departments__in = Department.objects.filter(pk = self.data['system'][3:]))]
        else:
            choices += [(pt.id, unicode(pt)) for pt in Employee.objects.all()]
        self.fields['employee'].choices = choices
        self.fields['employee'].required = False
        
class ActionOrderForm(forms.Form):

    assign_to = forms.ChoiceField(label=_("Employee"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    selected_action = forms.ChoiceField(label=_("Action"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    def __init__(self, *args, **kwargs):
        super(ActionOrderForm, self).__init__(*args, **kwargs)

        choices = [
            ('', _('Select employee')),
        ]
        choices += [(pt.id, unicode(pt)) for pt in Employee.objects.all()]
        self.fields['assign_to'].choices = choices

        choices = [
            ('', _('Select action')),
            ('AS', _('Assign to employee')),
            ('CA', _('Cancel assignment')),
            ('CW', _('Cancel work order')),
        ]
        self.fields['selected_action'].choices = choices

class SimpleSearchOrderForm(forms.Form):
    system = forms.ChoiceField(label=_("Department and System"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    def __init__(self, *args, **kwargs):
        super(SimpleSearchOrderForm, self).__init__(*args, **kwargs)

        choices = [
            ('', _('Select department')),
        ]
        choices += [('DE-%d' % pt.id, '%s: %s' % (_('Department'), pt)) for pt in Department.objects.all()]
        choices += [('SY-%d' % pt.id, '%s: %s' % (_('System'), pt)) for pt in System.objects.all()]
        self.fields['system'].choices = choices

class SimpleActionOrderForm(forms.Form):

    assign_to = forms.ChoiceField(label=_("Employee"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    def __init__(self, *args, **kwargs):
        
        department = kwargs.pop('department', None)

        super(SimpleActionOrderForm, self).__init__(*args, **kwargs)

        choices = [
            ('', _('Select employee')),
        ]
        if department:
            choices += [(pt.id, unicode(pt)) for pt in Employee.objects.filter(departments__in = department)]
        else:
            choices += [(pt.id, unicode(pt)) for pt in Employee.objects.all()]
        self.fields['assign_to'].choices = choices
