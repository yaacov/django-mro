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

from django import template
from django.conf import settings
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag(takes_context = True)
def bootstrap_breadcrumbs(context):
    '''
    Renders bootstrap breadcrumbs.

    Usage:
    {%  bootstrap_breadcrumbs %}
    '''
    
    # get the url path list
    path = context['request'].path.split('/')
    
    # remove none path parts and replace object-key 
    # path parts with the word "edit"
    path = path[1:-1]
    path_str = [ [p, _('edit')][p.isdigit()] for p in path]
    
    length = len(path)
    if length > 0:
        crumbs_html = u'<li><a href="/">%s</a><span class="divider">/</span></li>' % _('home')
    else:
        crumbs_html = u'<li class="active">%s</li>' % _('home')

    # check path length
    if length > 0:
        # create the crumbs list
        for i in range(length - 1):
            crumb_dict = {
                'text': _(path_str[i]),
                'url': '/'.join(path[:i + 1])
            }
            crumbs_html += u'<li><a href="/%(url)s/">%(text)s</a><span class="divider">/</span></li>' % crumb_dict
        
        # add the active path
        crumbs_html += u'<li class="active">%s</li>' % _(path_str[length - 1])
    
    # output as a list
    return '<ul class="breadcrumb">%s</ul>' % crumbs_html

@register.simple_tag
def bootstrap_paginator(table):
    '''
    Renders bootstrap table pagination.
    
    requires a django_tables2 table object
    
    Usage:
    {%  bootstrap_paginator table %}
    '''
    
    # check for table pages
    if table.paginator.num_pages < 2:
        return ''
    
    # collect page data
    paginator_html = u''

    try:
        current = table.page.number
    except:
        current = table.number
    prev = current - 1
    next = current + 1
    
    # render the prev button
    if prev >= 1:
        paginator_html += u'''<li>
            <a href="#" class="paginators" data-page="%d">%s</a></li>''' % (prev, _('Prev'))
    else:
        paginator_html += u'''<li class="active" >
            <a href="#" class="paginators" data-page="%d">%s</a></li>''' % (1, _('Prev'))
    
    # render the pages buttons
    for i in range(table.paginator.num_pages):
        if (i + 1) == current:
            paginator_html += u'''<li class="active" >
                <a href="#" class="paginators" data-page="%(page)d">%(page)d</a></li>''' % {'page': i + 1}
        else:
            paginator_html += u'''<li>
                <a href="#" class="paginators" data-page="%(page)d">%(page)d</a></li>''' % {'page': i + 1}
    
    # render the next button
    if next <= table.paginator.num_pages:
        paginator_html += u'''<li>
            <a href="#" class="paginators" data-page="%d">%s</a></li>''' % (next, _('Next'))
    else:
        paginator_html += u'''<li class="active" >
            <a href="#" class="paginators" data-page="%d">%s</a></li>''' % (table.paginator.num_pages, _('Next'))
    
    # output as a list
    return u'<div class="pagination"><ul>%s</ul></div>' % paginator_html

@register.simple_tag
def bootstrap_thumbnails(thumbnails):
    '''
    Renders bootstrap thumbnails.
    
    requires a queryset or a list
    
    Usage:
    {%  bootstrap_thumbnails thumbs %}
    '''
    
    thumbnails_html = ''
    is_query = type(thumbnails) != type(list())
    
    # create the thumbnail list
    for thumb in thumbnails:
        # if tumb is a query, trunslate to dict
        if is_query:
            thumb_dict = {
                'link': thumb.id,
                'image_url': thumb.image.url,
                'name': thumb.name,
                'description': thumb.description,
            }
        else:
            thumb_dict = {
                'link': thumb['link'],
                'image_url': thumb['image_url'],
                'name': _(thumb['name']),
                'description': _(thumb['description']),
            }
        
        thumbnails_html += u'''
        <li class="span3">
            <a class="thumbnail" href="%(link)s">
                <img src="%(image_url)s" alt="%(name)s icon">
            </a>
            <h4>%(name)s</h4>
            <p>%(description)s</p>
        </li>
        ''' % thumb_dict
    
    # output as a list
    return u'<ul class="thumbnails">%s</ul>' % thumbnails_html

@register.simple_tag
def bootstrap_list(items):
    '''
    Renders bootstrap items list.
    
    requires a queryset or a list
    
    Usage:
    {%  bootstrap_list items %}
    '''
    
    items_html = ''
    is_query = type(items) != type(list())
    
    # create the thumbnail list
    for item in items:
        # if tumb is a query, trunslate to dict
        if is_query:
            item_dict = {
                'link': item.id,
                'image_url': item.image.url,
                'name': item.name,
                'description': item.description,
            }
        else:
            item_dict = {
                'link': item['link'],
                'image_url': item['image_url'],
                'name': _(item['name']),
                'description': _(item['description']),
            }
        
        items_html += u'''
        <li class="span12">
            <dl class="dl-horizontal">
                <dt>
                    <a class="thumbnail" href="%(link)s">
                    <img src="%(image_url)s" alt="%(name)s icon">
                    </a>
                </dt>
                <dd>
                    <a href="%(link)s"><h4>%(name)s</h4></a>
                    <p>%(description)s</p>
                </dd>
            </dl>
        </li>
        ''' % item_dict
    
    # output as a list
    return u'<ul class="thumbnails">%s</ul>' % items_html

@register.simple_tag
def bootstrap_header(header):
    '''
    Renders bootstrap page header.
    
    requires a header dictionary
    
    Usage:
    {%  bootstrap_header header %}
    '''
    
    header_html = ''
    
    # check for header dict
    if type(header) != type(dict()):
        return ''
    
    # render the page header
    if 'thumb' in header.keys() and header['thumb']:
        header_html += u'''<p class="lead"><img src="%(thumb)s" alt="%(header)s"> %(header)s </p>''' % header
    else:
        header_html += u'''<h1>%(header)s</h1>''' % header
    
    # wrap with header div
    header_html = u'<div class="page-header">%s</div>' % header_html
    
    # add lead
    if 'lead' in header.keys() and header['lead']:
        header_html += u'''<p class="lead space">%(lead)s</p>''' % header
    else:
        header_html += u'''<p class="lead space"></p>'''
    
    # output as a list
    return header_html

