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

from django.utils.translation import ugettext as _
import django_tables2 as tables

from mro_contract.models import Contract

class ContractTable(tables.Table):
    number = tables.TemplateColumn(
        '''<a href="{{ record.pk }}/" >{{ record.number }}</a>''')
    #number.verbose_name = _('Number')

    slug = tables.TemplateColumn(
        '''{{ record }}''')
    slug.verbose_name = _('Contract')
    slug.orderable = False
    
    class Meta:
        model = Contract
        template = 'mro/table.html'
        attrs = {'class': 'table table-striped'}
        fields = ('number', 'slug', 'business', 'include_parts', 'start', 'end')
