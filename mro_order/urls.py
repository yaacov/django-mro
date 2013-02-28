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

urlpatterns = patterns('mro_order.views',
   
    url(r'^fracture/$', 'system', 
        {'action': 'table', 'work_type': 'fracture'}),
    url(r'^fracture/(?P<system_pk>\d+)/$', 'system_order', 
        {'action': 'table', 'work_type': 'fracture'}),
    url(r'^fracture/(?P<system_pk>\d+)/add/$', 'manage_fracture_order', 
        {'action': 'table', 'work_type': 'fracture'}),
    url(r'^fracture/(?P<system_pk>\d+)/(?P<order_pk>\d+)/$', 'manage_fracture_order', 
        {'action': 'table', 'work_type': 'fracture'}),

    url(r'^maintenance/$', 'system', 
        {'action': 'table', 'work_type': 'maintenance'}),
    url(r'^maintenance/(?P<system_pk>\d+)/$', 'system_order', 
        {'action': 'table', 'work_type': 'maintenance'}),
    url(r'^maintenance/(?P<system_pk>\d+)/add/(?P<maintenance_pk>\d+)/$', 'manage_maintenance_order', 
        {'action': 'table', 'work_type': 'maintenance'}),
    url(r'^maintenance/(?P<system_pk>\d+)/(?P<order_pk>\d+)/$', 'manage_maintenance_order', 
        {'action': 'table', 'work_type': 'maintenance'}),


    url(r'^(?P<order_id>\d+)/$', 'manage_order', 
        {'action': 'edit', 'work_type': 'maintenance'}),

    url(r'^maintenance/(?P<department_pk>\d+)/$', 'order_table', 
        {'action': 'table', 'work_type': 'maintenance'}),
    url(r'^maintenance/(?P<department_pk>\d+)/add/$', 'manage_order', 
        {'action': 'add', 'work_type': 'maintenance'}),
    url(r'^maintenance/(?P<department_pk>\d+)/delete/$', 'manage_order', 
        {'action': 'delete', 'work_type': 'maintenance'}),
    url(r'^maintenance/(?P<department_pk>\d+)/(?P<order_id>\d+)/$', 'manage_order', 
        {'action': 'edit', 'work_type': 'maintenance'}),
    
    url(r'^$', 'work'),
)

# breadcrumbs translation guide
breadcrumbs = (
    _('maintenance'),
    _('fracture'),
    _('new'),
)
