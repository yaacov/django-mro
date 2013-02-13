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

import os
from django.core.management.base import BaseCommand, CommandError
from mro_theme.file_list import STATIC_PATH, COMPRESSOR, COMPILER
from mro_theme.file_list import less_files, css_files, js_files
from mro_theme.file_list import output_css_file, output_js_file

class Command(BaseCommand):
    help = 'compile less files, and minify the css and js files'
    
    def concat_files(self, out_file_name, file_list):
        ''' concat number of resorce files into one big file
        '''
        
        # collect files
        out_file = open(out_file_name, 'wb')
        for f in file_list:
            # write all files into one file
            out_file.write(open(f).read())
        
    def handle(self, *args, **options):
        ''' run the command
        '''
        
        # compile and compress the less files
        for f in less_files:
            # calculate file base path
            base_file = os.path.join(STATIC_PATH, f)
            
            # compile
            less_file = '%s.less' % (base_file)
            css_file = '%s.css' % (base_file)
            compile_cmd = '%s %s > %s' % (COMPILER, less_file, css_file)
            os.system(compile_cmd)
        
        # empty the collected files list
        collected_files = []
        
        # compress the css files
        for f in css_files:
            # calculate file base path
            base_file = os.path.join(STATIC_PATH, f)
            
            # compress
            css_file = '%s.css' % (base_file)
            compress_file = '%s.min.css' % (base_file)
            compress_cmd = '%s %s > %s' % (COMPRESSOR, css_file, compress_file)
            os.system(compress_cmd)
            
            # collect the compressed file
            collected_files.append(compress_file)
            
        # concat minified css files
        file_name = os.path.join(STATIC_PATH, output_css_file)
        self.concat_files(file_name, collected_files)
        
        # empty the collected files list
        collected_files = []
        
        # compress the js files
        for f in js_files:
            # calculate file base path
            base_file = os.path.join(STATIC_PATH, f)
            
            # compress
            js_file = '%s.js' % (base_file)
            compress_file = '%s.min.js' % (base_file)
            compress_cmd = '%s %s > %s' % (COMPRESSOR, js_file, compress_file)
            os.system(compress_cmd)
            
            # collect the compressed file
            collected_files.append(compress_file)

        # concat minified js files
        file_name = os.path.join(STATIC_PATH, output_js_file)
        self.concat_files(file_name, collected_files)
        
