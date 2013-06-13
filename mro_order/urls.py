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
from django.views.generic import RedirectView

from mro_order.views import PrintOrders

urlpatterns = patterns('mro_order.views',
    
    url(r'^issue/$', 'issue'),
    url(r'^issue/(?P<system_pk>\d+)/$', 'issue_order'),
    url(r'^issue/(?P<system_pk>\d+)/add/$', 'manage_issue_order'),
    url(r'^issue/(?P<system_pk>\d+)/add/(?P<maintenance_pk>\d+)/$', 'manage_issue_order'),
    url(r'^issue/(?P<system_pk>\d+)/(?P<order_pk>\d+)/$', 'manage_issue_order'),

    url(r'^assign/$', 'assign'),
    url(r'^assign/(?P<system_pk>\d+)/$', RedirectView.as_view(url='/order/assign/')),
    url(r'^assign/(?P<system_pk>\d+)/(?P<order_pk>\d+)/$', 'manage_issue_order', 
        {
            'next_url': '/order/assign/',
            'update_url': '/order/assign/'
        }),

    url(r'^print/$', PrintOrders.as_view()),
    url(r'^print/(?P<system_pk>\d+)/$', RedirectView.as_view(url='/order/print/')),
    url(r'^print/(?P<system_pk>\d+)/(?P<order_pk>\d+)/$', 'manage_issue_order', 
        {
            'next_url': '/order/print/',
            'update_url': '/order/print/'
        }),

    url(r'^status/$', 'status'),
    url(r'^status/(?P<system_pk>\d+)/$', RedirectView.as_view(url='/order/status/')),
    url(r'^status/(?P<system_pk>\d+)/(?P<order_pk>\d+)/$', 'manage_issue_order', 
        {
            'next_url': '/order/status/',
            'update_url': '/order/status/'
        }),
    
    url(r'^table/$', 'table'),
    url(r'^table/orders/$', 'table_orders'),
    url(r'^table/orders/(?P<system_pk>\d+)/$', RedirectView.as_view(url='/order/table/orders/')),
    url(r'^table/orders/(?P<system_pk>\d+)/(?P<order_pk>\d+)/$', 'manage_issue_order', 
        {
            'next_url': '/order/table/orders/',
            'update_url': '/order/table/orders/'
        }),

    url(r'^$', 'order'),
)

# breadcrumbs translation guide
breadcrumbs = (
    _('issue'),
    _('add'),
    _('assign'),
    _('print'),
    _('status'),
    _('table'),
    _('orders'),
)
