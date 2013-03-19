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

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

class Department(models.Model):
    """
    department
    
    all objects in the system can be mapped to a specific department
    
    e.g. an equipment belongs to a department, an employee works in 
        a department etc...
    """
    
    # identification
    name = models.CharField(_('Name'), max_length = 30, unique = True)
    description = models.TextField(_('Description'))
    
    # image - profile image or logo
    image = models.ImageField(upload_to='departments/', blank = True, null = True)
    image.verbose_name = _('Image')
    
    # model overides
    def __unicode__(self):
        return '%s' % (self.name)
    
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ('name',)

class Employee(models.Model):
    """
    an employee
    
    contact information for an employee
    """
    
    # name
    first_name = models.CharField(_('First Name'), 
        max_length = 30)
    last_name = models.CharField(_('Last Name'), 
        max_length = 30, blank = True, null = True)
    
    # contact information
    phone = models.CharField(_('Phone'), 
        max_length = 30, blank = True, null = True)
    cell_phone = models.CharField(_('Cell Phone'), 
        max_length = 30, blank = True, null = True)
    address = models.CharField(_('Address'), 
        max_length = 30, blank = True, null = True)
    email = models.EmailField(_('Email'), 
        max_length = 30, blank = True, null = True)
    
    # image - profile image or profile icon
    image = models.ImageField(null=True, blank=True, upload_to='contacts/')
    image.verbose_name = _('Image')
    
    # departments
    departments = models.ManyToManyField(Department, blank = True, null = True)
    departments.verbose_name = _('Department')
    
    def department_list(self):
        out = []
        for department in self.departments.all():
            if department.name:
                out.append(department.name)
        return ', '.join(out)
    department_list.short_description = _('Departments')
    
    # model overides
    def __unicode__(self):
        if self.last_name:
            return '%s, %s' % (self.first_name, self.last_name)
        else:
            return '%s' % (self.first_name)
    
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ('first_name', 'last_name',)

class Business(models.Model):
    """
    a business
    
    contact information for a business
    """
    
    # name
    name = models.CharField(_('Name'), 
        max_length = 30)
    contact_person = models.CharField(_('Contact person'), 
        max_length = 30)

    # contact information
    phone = models.CharField(_('Phone'), 
        max_length = 30, blank = True, null = True)
    fax = models.CharField(_('Fax'), 
        max_length = 30, blank = True, null = True)
    address = models.CharField(_('Address'), 
        max_length = 30, blank = True, null = True)
    email = models.EmailField(_('Email'), 
        max_length = 30, blank = True, null = True)
    
    # image - profile image or profile icon
    image = models.ImageField(null=True, blank=True, upload_to='contacts/')
    image.verbose_name = _('Image')
    
    # departments
    departments = models.ManyToManyField(Department, blank = True, null = True)
    departments.verbose_name = _('Department')
    
    def department_list(self):
        out = []
        for department in self.departments.all():
            if department.name:
                out.append(department.name)
        return ', '.join(out)
    department_list.short_description = _('Departments')
    
    # model overides
    def __unicode__(self):
        return '%s' % (self.first_name)
    
    class Meta:
        verbose_name = _('Business')
        verbose_name_plural = _('Businesses')
        ordering = ('name',)
