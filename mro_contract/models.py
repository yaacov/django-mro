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

from mro_contact.models import Department, Employee, Business

class Contract(models.Model):
    '''contract
    '''
    
    # the priority identification string
    number = models.CharField(_('Contract number'), max_length = 30, unique = True)
    
    # for this maintenance information
    business = models.ForeignKey(Business, verbose_name = _('Business'))
    
    # this contract include parts
    include_parts = models.BooleanField(_('Include parts'), default = False)
    
    # description
    description =  models.TextField(_('Document description'), blank = True, null = True)

    # contract dates
    start = models.DateField(default = lambda: date.today())
    start.verbose_name = _('Start date')

    end = models.DateField(default = lambda: date.today() + timedelta(days = 365))
    end.verbose_name = _('End date')

    # documents for this job
    documents = models.ManyToManyField('ContractDocument', related_name = 'contract_documents')
    documents.verbose_name = _('Documents')

    # model overides
    def __unicode__(self):
        if self.include_parts:
            return '%s-%s-%s' % (self.number, self.business, _('Include parts'))

        return '%s-%s' % (self.number, self.business)
    
    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')
        ordering = ('number',)

class ContractDocument(models.Model):
    ''' Documents used for the Contract
    '''
    # connection
    contract = models.ForeignKey(Contract)
    contract.verbose_name = _('Contract')

    # description
    title = models.CharField(_('Document title'), max_length = 30)
    description =  models.TextField(_('Document description'), blank = True, null = True)
    created = models.DateField(default = lambda: date.today())
    created.verbose_name = _('Created date')
    
    # the document
    image = models.FileField(null = True, blank = True, upload_to = 'documents/%Y/%m/%d')
    image.verbose_name = _('Document')

    class Meta:
        verbose_name = _('Contract Document')
        verbose_name_plural = _('Contract Documents')
        ordering = ('title',)
