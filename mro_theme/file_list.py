# -*- coding:utf-8 -*-

import os

# a list of static resource files used by this theme
# use the admin command:
#    ./manage.py compile_less
# to compile and commpres the static resource files.
# chenge the settings:
#    USE_MINIFY = True
# to make the theme base.html template use the commpressed files

# all input and output files are under the STATIC_PATH
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_PATH = os.path.join(FILE_PATH, 'static')

# the less compiler and compressor
COMPRESSOR = 'yui-compressor'
COMPILER = 'lessc'

# less files to compile
# without the .less postfix
less_files = [
    'bootstrap/less/bootstrap',
    'bootstrap/less/responsive', 
    'datepicker/less/datepicker',
]

# css files to minify
# without the .css postfix
css_files = [
    'bootstrap/less/bootstrap',
    'bootstrap/less/responsive',
    'datepicker/less/datepicker',
    'datepicker/less/datepicker',
    'sijpinner/css/sijpinner',
    'select2/select2',
    'mro/extra',
]

# javascript files to minify
# without the .js postfix
js_files = [
    'jquery/jquery',

    'bootstrap/js/bootstrap-transition',
    'bootstrap/js/bootstrap-alert',
    'bootstrap/js/bootstrap-modal',
    'bootstrap/js/bootstrap-dropdown',
    'bootstrap/js/bootstrap-scrollspy',
    'bootstrap/js/bootstrap-tab',
    'bootstrap/js/bootstrap-tooltip',
    'bootstrap/js/bootstrap-popover',
    'bootstrap/js/bootstrap-button',
    'bootstrap/js/bootstrap-collapse',
    'bootstrap/js/bootstrap-carousel',
    'bootstrap/js/bootstrap-typeahead',
    'datepicker/js/bootstrap-datepicker',
    'sijpinner/js/sijpinner',
    'select2/select2'
]

# outut files for the compiled and minified sources
output_css_file = 'mro/mro.min.css'
output_js_file = 'mro/mro.min.js'

