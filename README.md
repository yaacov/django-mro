Maintenance, Repair, and Operations
===================================

A Django progect for managing Maintenance, Repair, and Operations.

Tweaks to the standard Django settings

import the global settings
import django.conf.global_settings as DEFAULT_SETTINGS

get the project install path
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

External helper applications

crispy_forms - help render forms
django_tables2 - help render tables
south - data base migration tools
django_wsgiserver - CherryPy wsgi web server

Notes on building a new Django project
======================================

Create a new virtual env

Install python and the virtualenv python package

Init a new virtualenv 
virtualenv django-<project-name>
cd django-<project-name>

Activate the virtual environment
source ./bin/activate

Install required software
pip install <requirements>

Create the new django project

Start a new project
django-admin.py startproject <project-name>
cd <project-name>
chmod ugo+x manage.py

Add an application to the project
./manage.py startapp <app-name>

Localization
mkdir locale
./manage.py makemessages -l he
./manage.py compilemessages

Init Data Base and migrations
./manage.py schemamigration --initial <app-name>
./manage.py syncdb
./manage.py migrate

Update Data Base and migrations
./manage.py schemamigration --auto <app-name>
./manage.py migrate

Running the new application

./manage.py runserver

License
=======

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

Copyright (C) 2013 Yaacov Zamir <kobi.zamir@gmail.com>
Author: Yaacov Zamir (2013) <kobi.zamir@gmail.com>
