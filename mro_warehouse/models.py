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

class Item(models.Model):
    ''' a item stored in a warehouse
    '''
    
    UNITS = (
        ('PC', ugettext('pcs')),
        ('LI', ugettext('lit')),
        ('KG', ugettext('Kg')),
        ('ME', ugettext('m')),
    )
    
    # item information
    name = models.CharField(_('Name'), max_length = 30, unique = True)
    catalogic_number = models.CharField(_('Item catalog number'), max_length = 30, unique = True)
    unit = models.CharField(max_length = 2, choices = UNITS, default = 'PC')
    unit.verbose_name = _('Unit')
    description = models.CharField(_('Description'), max_length = 200, null = True, blank = True)
    
    unit_price = models.FloatField(null = True, blank = True, default = 0.0)
    unit_price.verbose_name = _('Unit Price')

    # image - item image
    image = models.ImageField(null=True, blank=True, upload_to='warehouse')
    image.verbose_name = _('Image')
    
    def unit_str(self):
        ''' human readable text representing a unit
        '''
        # get state_type information
        unit = self.unit
        
        # print out the work type and work_state
        if unit:
            return u'%s' % dict(self.UNITS)[unit]
        else:
            return ''
    unit_str.verbose_name = _('Unit')
    
    # model overrides
    def __unicode__(self):
        return u'%s %s %s' % (self.name, _('C.N.'), self.catalogic_number)
    
    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        ordering = ('name',)

class Warehouse(models.Model):
    ''' an warehouse
    '''
    
    # the warehouse identification
    name = models.CharField(_('Warehouse Name'), max_length = 30)
    
    # contact information
    phone = models.CharField(_('Phone'), 
        max_length = 30, blank = True, null = True)
    address = models.CharField(_('Address'), 
        max_length = 30, blank = True, null = True)
    email = models.EmailField(_('Email'), 
        max_length = 30, blank = True, null = True)
    
    # image - profile image or profile icon
    image = models.ImageField(null=True, blank=True, upload_to='warehouse')
    image.verbose_name = _('Image')
    
    # a list of items stored in the warehouse
    itmes = models.ManyToManyField(Item, related_name = 'warehouse_itmes', through = 'WarehouseItem')
    itmes.verbose_name = _('Warehouse Item')
    
    def __unicode__(self):
        return '%s' % (self.name,)
    
    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')
        ordering = ('name',)

class WarehouseItem(models.Model):
    ''' an item in the warehouse
    '''
    
    # connection
    warehouse = models.ForeignKey(Warehouse)
    warehouse.verbose_name = _('Warehouse')
    item = models.ForeignKey(Item, related_name = 'warehouse_item')
    item.verbose_name = _('Item')
    
    # how many items of this type are in the warehouse
    amount = models.IntegerField(_('Amount'), default = 1)
    
    # location of the item
    shelve = models.CharField(_('Shelve'), max_length = 30, null = True, blank = True)
    batch = models.CharField(_('Batch'), max_length = 30, null = True, blank = True)
    
    # dates
    entered = models.DateField(default=lambda: datetime.today(), null = True, blank = True)
    entered.verbose_name = _('Entered')
    expires = models.DateField(default=lambda: datetime.today() + timedelta(days = 365), null = True, blank = True)
    expires.verbose_name = _('Expires')
    
    class Meta:
        verbose_name = _('Warehouse Item')
        verbose_name_plural = _('Warehouse Items')
        ordering = ('warehouse',)
        unique_together = ('warehouse', 'item', 'shelve', 'batch')
