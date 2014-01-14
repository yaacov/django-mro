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

from django.conf.urls import patterns, url, include
#from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns('mro_system_type.views',
    
    url(r'^$', 'system_type'),
    url(r'^add/$', 'manage_system_type'),
    url(r'^(?P<system_type_pk>\d+)/$', 'manage_system_type'),
    url(r'^(?P<system_type_pk>\d+)/delete/$', 'manage_system_type_delete'),
    url(r'^add/delete/$', 'manage_system_type_delete'),

    url(r'^(?P<system_type_pk>\d+)/(?P<maintenance_type_pk>\d+)/$', 'manage_system_type_maintenance'),

#    url(r'^run/$', 'run_cron'),
)

# breadcrumbs translation guide
breadcrumbs = (
    _('system type'),
    _('maintenance'),
    _('delete'),
)
