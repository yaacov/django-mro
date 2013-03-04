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

from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns('mro_report.views',
    
    url(r'^$', 'report'),
    url(r'^warehouse_log/$', 'warehouse_log'),
    url(r'^system_maintenance/$', 'system_maintenance'),
    url(r'^system_maintenance/(?P<system_pk>\d+)/$', 'system_maintenance_report'),
    url(r'^system_document/$', 'system_document'),
    url(r'^system_document/(?P<system_pk>\d+)/$', 'system_document_report'),
)

# breadcrumbs translation guide
breadcrumbs = (
    _('warehouse_log'),
    _('system_maintenance'),
    _('system_document'),
)
