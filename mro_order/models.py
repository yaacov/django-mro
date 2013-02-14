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

from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from mro_contact.models import Department, Employee, Suplier
from mro_warehouse.models import Item, Warehouse, WarehouseItem
from mro_equipment.models import Equipment, Priority

class Order(models.Model):
    ''' work order
        
        an actual work to do
    '''
    
    ORDER_STATE = (
        ('RE', _('Reported')),
        ('AS', _('Assigned')),
        ('CO', _('Completed')),
        ('HO', _('Holding')),
        ('CA', _('Canceled')),
    )
    
    WORK_TYPE = (
        ('NE', _('New')),
        ('MA', _('Maintenance')),
        ('FR', _('Fracture')),
    )
    
    # this work is on this equipment
    equipment = models.ForeignKey(Equipment)
    equipment.verbose_name = _('Equipment')
    
    # when to do the job
    work_type = models.CharField(max_length = 2, choices = WORK_TYPE, default = 'MA')
    work_type.verbose_name = _('Work type')
    
    # estimated time to complete the job
    estimated_work_time = models.IntegerField(_('Estimated work hours'), default = 8)
    
    # is this a priority job
    priority = models.ForeignKey(Priority)
    priority.verbose_name = _('Priority')
    
    # the job manager and contact information
    assign_to = models.ForeignKey(Employee, null = True, blank = True)
    assign_to.verbose_name = _('Assign to')
    
    # job state
    work_order_state = models.CharField(max_length = 2, choices = ORDER_STATE, default = 'FR')
    work_order_state.verbose_name = _('Work state')
    
    # estimated completion can be calculated using work start and work time
    estimated_completion  = models.DateField(default=lambda: datetime.today() + timedelta(days = 2))
    estimated_completion .verbose_name = _('Estimated completion')
    
    # when job was reported and done
    created = models.DateField(default=lambda: datetime.today())
    created.verbose_name = _('Created')
    assigned = models.DateField(blank = True, null = True)
    assigned.verbose_name = _('Assigned')
    completed = models.DateField(blank = True, null = True)
    completed.verbose_name = _('Completed')
    
    # what to do
    work_description = models.TextField(_('Work description'))
    
    # special notes about this job
    work_notes = models.TextField(_('Special notes'), null = True, blank = True)
    
    # how many work hours where put into this job by employees
    employees = models.ManyToManyField(Employee, related_name = 'order_employees', through = 'OrderEmployee')
    employees.verbose_name = _('Order employee')
    
    # items needed to complete this job
    itmes = models.ManyToManyField(Item, related_name = 'order_itmes', through = 'OrderItem')
    itmes.verbose_name = _('Order item')
    
    def work_order_state_str(self):
        ''' human readable text representing a work_order_state
        '''
        # get state_type information
        work_order_state = self.work_order_state
        
        # print out the work type and work_state
        if work_order_state:
            return u'%s' % dict(self.WORK_STATE)[work_order_state]
        else:
            return u''
        
    work_order_state_str.verbose_name = _('Work state')
    
    # model overides
    def __unicode__(self):
        return u'%s %s' % (self.equipment.name, self.created)
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('equipment',)

class OrderItem(models.Model):
    ''' Items used for the Order
    '''
    
    # connection
    order = models.ForeignKey(Order)
    order.verbose_name = _('Order')
    item = models.ForeignKey(Item, related_name = 'order_item')
    item.verbose_name = _('Item')
    
    # amount of items used
    issued = models.DateField(default=lambda: datetime.today())
    issued.verbose_name = _('Issued')
    amount = models.IntegerField(_('Amount'), default = 1)
    
    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ('order',)

class OrderEmployee(models.Model):
    ''' employees working on a job
    
        actual work hours put in the job by employees
    '''
    
    WORK_TYPE = (
        ('OS', _('On site')),
        ('OF', _('Office')),
    )
    
    # connection
    order = models.ForeignKey(Order)
    order.verbose_name = _('Order')
    employee = models.ForeignKey(Employee, related_name = 'work_employee')
    employee.verbose_name = _('Employee')
    
    # how many hours where worked and some information
    work_started = models.DateField(default=lambda: datetime.today())
    work_type = models.CharField(max_length = 2, choices = WORK_TYPE, default = 'OS')
    work_type.verbose_name = _('Order type')
    work_hours = models.IntegerField(_('Order hours'), default = 1)
    
    def work_type_str(self):
        ''' human readable text representing a work_type
        '''
        # get work_type information
        work_type = self.work_type
        
        # print out the work type and work_count
        if work_type:
            return u'%s' % dict(self.WORK_TYPE)[work_type]
        else:
            return ''
    work_type_str.verbose_name = _('Work type')
    
    class Meta:
        verbose_name = _('Order employee')
        verbose_name_plural = _('Order employees')
        ordering = ('order',)

