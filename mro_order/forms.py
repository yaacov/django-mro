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

from mro_system.models import Maintenance
from mro_system.models import System
from mro_system.models import Priority
from mro_system.models import Item
from mro_system.models import MaintenanceItem
from mro_system.models import Equipment

class OrderForm(ModelForm):
    can_delete = True

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['equipment'].widget = forms.HiddenInput()
        self.fields['maintenance'].widget = forms.HiddenInput()

    work_started_time = forms.CharField(required=False)
    work_started_time.label=_('Work start time')
    
    def clean_work_started_time(self):
        work_started_time = str(self.cleaned_data['work_started_time'])
        if not work_started_time:
            return None
        
        if work_started_time.find(':') == -1:
            work_started_time = work_started_time[:2] + ':' + work_started_time[2:]
        
        return work_started_time
    
    work_end_time = forms.CharField(required=False)
    work_end_time.label=_('Work end time')
    
    def clean_work_end_time(self):
        work_end_time = str(self.cleaned_data['work_end_time'])
        if not work_end_time:
            return None
        
        if work_end_time.find(':') == -1:
            work_end_time = work_end_time[:2] + ':' + work_end_time[2:]
        
        return work_end_time
    
    class Meta:
        model = Order
        fields = ('work_number', 
            'equipment', 'maintenance', 
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
    equipment = forms.ChoiceField(label=_("Department and Equipment"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    employee = forms.ChoiceField(label=_("Employee"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    work_order_state = forms.ChoiceField(label=_("Work state"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    def clean_work_order_state(self):
        work_order_state = str(self.cleaned_data['work_order_state'])
        if not work_order_state:
            return 'RE'
        
        return work_order_state
    
    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)
        
        choices = [
            ('AL', _('Select work state')),
            ('', _('Waiting for assignment')), # RE
            ('AS', _('Assigned')),
            ('CO', _('Completed')),
            ('CA', _('Canceled')),
        ]
        self.fields['work_order_state'].choices = choices
        
        choices = [
            ('', _('Department/Equipment')),
        ]
        choices += [('DE-%d' % pt.id, '%s: %s' % (_('Department'), pt)) for pt in Department.objects.all()]
        choices += [('EQ-%d' % pt.id, '%s: %s' % (_('Equipment'), pt)) for pt in Equipment.objects.all()]
        self.fields['equipment'].choices = choices

        instance = getattr(self, 'instance', None)
        choices = [
            ('', _('Select employee')),
        ]
        
        if 'equipment' in self.data:
            try:
                choices += [(u'%d' % pt.id, u'%s' % (pt)) for pt in 
                    Employee.objects.filter(departments__in = Department.objects.filter(pk = self.data['equipment'][3:]))]
            except:
                choices += [(pt.id, unicode(pt)) for pt in Employee.objects.all()]
        else:
            choices += [(pt.id, unicode(pt)) for pt in Employee.objects.all()]
        
        self.fields['employee'].choices = choices
        self.fields['employee'].required = False
        
class ActionOrderForm(forms.Form):

    assign_to = forms.ChoiceField(label=_("Employee"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    selected_action = forms.ChoiceField(label=_("Action"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    def clean_selected_action(self):
        selected_action = str(self.cleaned_data['selected_action'])
        if not selected_action:
            return 'AS'
        
        return selected_action
        
    def __init__(self, *args, **kwargs):
        super(ActionOrderForm, self).__init__(*args, **kwargs)

        choices = [
            ('', _('Select employee')),
        ]
        choices += [(pt.id, unicode(pt)) for pt in Employee.objects.all()]
        self.fields['assign_to'].choices = choices

        choices = [
            ('NONE', _('Select action')),
            ('', _('Assign to employee')),
            ('CO', _('Work completed')),
            ('CA', _('Cancel assignment')),
            ('CW', _('Cancel work order')),
        ]
        self.fields['selected_action'].choices = choices

class SimpleSearchOrderForm(forms.Form):
    equipment = forms.ChoiceField(label=_("Department and Equipment"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))

    employee = forms.ChoiceField(label=_("Employee"), required = False, choices=(),
        widget=forms.Select(attrs={'class':'selector'}))
    
    def __init__(self, *args, **kwargs):
        super(SimpleSearchOrderForm, self).__init__(*args, **kwargs)

        choices = [
            ('', _('Department/Equipment')),
        ]
        choices += [('DE-%d' % pt.id, '%s: %s' % (_('Department'), pt)) for pt in Department.objects.all()]
        choices += [('EQ-%d' % pt.id, '%s: %s' % (_('Equipment'), pt)) for pt in Equipment.objects.all()]
        self.fields['equipment'].choices = choices
        
        choices = [
            ('', _('Select employee')),
        ]
        
        if 'equipment' in self.data:
            try:
                choices += [(u'%d' % pt.id, u'%s' % (pt)) for pt in 
                    Employee.objects.filter(departments__in = Department.objects.filter(pk = self.data['equipment'][3:]))]
            except:
                choices += [(pt.id, unicode(pt)) for pt in Employee.objects.all()]
        else:
            choices += [(pt.id, unicode(pt)) for pt in Employee.objects.all()]
        
        self.fields['employee'].choices = choices
        self.fields['employee'].required = False
        
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
        
