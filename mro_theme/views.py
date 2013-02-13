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
from django.utils.translation import ugettext_noop
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

def collect_thumbs():
    """
    Check for header info in the installed apps
    """
    
    # init an empty thumbs list
    thumbs = []
    
    # get all module applications
    apps = [app for app in settings.INSTALLED_APPS if app.startswith('mro_')]
    
    # check if the module has thumb data in its' orgenizer.py file
    for app in apps:
        try:
            # try to import the module
            module = __import__('%s.views' % app, globals(), locals(), ['thumb'], -1)
            
            # check for thumb dict
            if type(module.thumb) == type(dict()):
                thumbs.append(module.thumb)
        except:
            pass
    
    return thumbs
    
# views
def home(request):
    """
    start page
    
    display the start page as a table/list of thumbnails
    """
    
    response_dict = {}

    response_dict['headers'] = {
        'header': _('Start'),
        'lead': _('Organizer start page. Choose the operation.'),
        'thumb': False,
    }
    
    # read modules thumbs data
    response_dict['thumbs'] = collect_thumbs()
    
    return render(request, 'mro/base_thumbs.html', response_dict)

