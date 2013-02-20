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
from django.template.loader import get_template
from django.conf import settings

from mro_theme.models import Project

register = template.Library()

@register.simple_tag()
def add_header_js():
    '''
    Renders java script 

    Usage:
    {%  add_header_js %}
    '''
    
    c = template.Context({ 'STATIC_URL': settings.STATIC_URL })

    if settings.USE_MINIFY:
        t = get_template('mro/base_js_min.html')
    else:
        t = get_template('mro/base_js.html')

    # render
    return t.render(c)

@register.simple_tag()
def add_header_css():
    '''
    Renders style sheets

    Usage:
    {%  add_header_css %}
    '''
    
    c = template.Context({ 'STATIC_URL': settings.STATIC_URL })

    if settings.USE_MINIFY:
        t = get_template('mro/base_css_min.html')
    else:
        t = get_template('mro/base_css.html')

    # render
    return t.render(c)

@register.simple_tag()
def project_name():
    '''
    Renders application name

    Usage:
    {%  project_name %}
    '''
    
    project = Project.objects.get()

    # render
    if project:
        return project.name

    return u'M.R.O'

@register.simple_tag()
def copyright_notice():
    '''
    Renders copyright notice

    Usage:
    {%  copyright_notice %}
    '''

    project = Project.objects.get()

    # render
    if project:
        return u'&copy; %s' % project.copyright
    
    return u'&copy; M.R.O 2013'
