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

from datetime import date, datetime, timedelta

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from mro_contact.models import Department, Employee, Suplier
from mro_warehouse.models import Item, Warehouse, WarehouseItem
from mro_system.models import System, Priority, Maintenance

class Order(models.Model):
    ''' work order
        
        an actual work to do
    '''
    
    ORDER_STATE = (
        ('RE', _('Waiting for assignment')),
        ('AS', _('Assigned')),
        ('CO', _('Completed')),
        ('HO', _('Holding')),
        ('CA', _('Canceled')),
    )
    
    # this work is on this system
    system = models.ForeignKey(System)
    system.verbose_name = _('System')
    
    # for this maintenance information
    maintenance = models.ForeignKey(Maintenance, null = True, blank = True)
    maintenance.verbose_name = _('Maintenance')

    # estimated time to complete the job
    estimated_work_time = models.IntegerField(_('Estimated work hours'), default = 8)
    
    # is this a priority job
    priority = models.ForeignKey(Priority)
    priority.verbose_name = _('Priority')
    
    # the job contract information
    contract_number = models.CharField(_('Contract number'), max_length = 30, null = True, blank = True)
    contract_include_parts = models.BooleanField(_('Contract include parts'))

    # the job manager and contact information
    assign_to = models.ForeignKey(Employee, null = True, blank = True)
    assign_to.verbose_name = _('Assign to Employee')
    
    assign_to_suplier = models.ForeignKey(Suplier, null = True, blank = True)
    assign_to_suplier.verbose_name = _('Assign to Suplier')

    # job state
    work_order_state = models.CharField(max_length = 2, choices = ORDER_STATE, default = 'RE')
    work_order_state.verbose_name = _('Work state')
    
    # estimated completion can be calculated using work start and work time
    estimated_completion  = models.DateField(default=lambda: date.today() + timedelta(days = 2))
    estimated_completion .verbose_name = _('Estimated completion')
    
    # when job was reported and done
    created = models.DateField(default=lambda: date.today())
    created.verbose_name = _('Created date')
    assigned = models.DateField(blank = True, null = True)
    assigned.verbose_name = _('Assigned date')
    completed = models.DateField(blank = True, null = True)
    completed.verbose_name = _('Completed date')
    
    # what to do
    work_description = models.TextField(_('Work description'))
    
    # special notes about this job
    work_notes = models.TextField(_('Special notes'), null = True, blank = True)
    
    # how many work hours where put into this job by employees
    employees = models.ManyToManyField(Employee, related_name = 'order_employees', through = 'OrderEmployee')
    employees.verbose_name = _('Order employee')
    
    # items needed to complete this job
    items = models.ManyToManyField(Item, related_name = 'order_items', through = 'OrderItem')
    items.verbose_name = _('Order item')
    
    # documents for this job
    documents = models.ManyToManyField('OrderDocument', related_name = 'order_documents')
    documents.verbose_name = _('Documents')

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
    
    def save(self, *args, **kwargs):
        
        # check if assigned to worker
        if self.assign_to and self.work_order_state in ['RE']:
            self.work_order_state = 'AS'

        # adjast work state
        if self.assigned and self.work_order_state in ['RE']:
            self.work_order_state = 'AS'
        if self.completed and self.work_order_state in ['RE', 'AS']:
            self.work_order_state = 'CO'

        # check dates for work state
        if not self.assigned and self.work_order_state == 'AS':
            self.assigned = date.today()
        if not self.completed and self.work_order_state == 'CO':
            self.completed = date.today()

        # check if order complete
        if self.pk is not None:
            orig = Order.objects.get(pk=self.pk)
            if self.maintenance and orig.work_order_state != 'CO' and  self.work_order_state == 'CO':
                self.maintenance.last_maintenance_counter_value = self.maintenance.current_counter_value
                self.maintenance.save()

        if (self.maintenance and self.completed and
                (not self.maintenance.last_maintenance or 
                    self.maintenance.last_maintenance < self.completed)):
            self.maintenance.last_maintenance = self.completed
            self.maintenance.save()

        # call the default save method
        super(Order, self).save(*args, **kwargs)

    # model overides
    def __unicode__(self):
        short_desc = u' '.join(self.work_description.split('\n')[0].split()[:7])
        return u'%s' % short_desc
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('system',)

class OrderItem(models.Model):
    ''' Items used for the Order
    '''
    
    # connection
    order = models.ForeignKey(Order)
    order.verbose_name = _('Order')
    item = models.ForeignKey(Item, related_name = 'order_item')
    item.verbose_name = _('Item')
    
    # date of order
    ordered = models.DateField(default = lambda: date.today())
    ordered.verbose_name = _('Ordered on date')

    # date ot delivery
    issued = models.DateField(null = True, blank = True)
    issued.verbose_name = _('Issued on date')
    
    # amount of items used
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
    
    # a number atached to this work
    work_number = models.CharField(_('Work number'), max_length = 10, null = True, blank = True)

    # connection
    order = models.ForeignKey(Order)
    order.verbose_name = _('Order')
    employee = models.ForeignKey(Employee, related_name = 'work_employee')
    employee.verbose_name = _('Employee')
    
    # how many hours where worked and some information
    work_started = models.DateField(_('Work started'), default=lambda: date.today())
    work_type = models.CharField(max_length = 2, choices = WORK_TYPE, default = 'OS')
    work_type.verbose_name = _('Order type')
    work_hours = models.IntegerField(_('Order hours'), default = 1)
    
    # admin stuff
    work_started_time = models.TimeField(_('Work start time'), blank = True, null = True)
    work_end_time = models.TimeField(_('Work end time'), blank = True, null = True)

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

class OrderDocument(models.Model):
    ''' Documents used for the Order
    '''
    # connection
    order = models.ForeignKey(Order)
    order.verbose_name = _('Order')

    # description
    title = models.CharField(_('Document title'), max_length = 30)
    description =  models.TextField(_('Document description'), blank = True, null = True)
    created = models.DateField(default=lambda: date.today())
    created.verbose_name = _('Created date')
    
    # the document
    image = models.FileField(null=True, blank=True, upload_to='documents/%Y/%m/%d')
    image.verbose_name = _('Document')

    class Meta:
        verbose_name = _('Order Document')
        verbose_name_plural = _('Order Documents')
        ordering = ('title',)