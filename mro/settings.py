# Django settings for mro project.
# -*- coding:utf-8 -*-

import os
import sys
import django.conf.global_settings as DEFAULT_SETTINGS

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
SITE_URL = "/mro/"

# add the dist-packages path the the python path
sys.path.insert(1,'%s/dist-packages' % SITE_ROOT)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Yaacov Zamir', 'kobi.zamir@gmail.com'),
)

EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER="kobi.zamir@gmail.com"
EMAIL_HOST_PASSWORD="PASSWORD!!"
EMAIL_USE_TLS=True

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'main.sqlite'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Asia/Jerusalem'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'he'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Overide the USE_L10N defaults. If the system language (USE_L10N settings) 
# is what you need, remove the DATE_INPUT_FORMATS overide
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y-%m-%d', '%d/%m/%y', '%b %d %Y',
'%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
'%B %d, %Y', '%d %B %Y', '%d %B, %Y')

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media') + '/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static') + '/'
STATICFILES_ROOT = os.path.join(SITE_ROOT, 'static') + '/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/' 

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xr%yzm0b#fviav*whr008tt*+8251=3ryq-oif$4uxid1@t7wy'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'mro.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mro.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'import_export',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'crispy_forms',
    'django_tables2',
    'wkhtmltopdf',

    'mro',
    'mro_icons',
    'mro_theme',
    'mro_order',
    'mro_system',
    'mro_system_card',
    'mro_contact',
    'mro_warehouse',
    'mro_contract',
    'mro_report',

    # server things
    'django_cron',
    #'django_wsgiserver',

    # migration manager
    'south', # must be at the END
)

CRON_CLASSES = [
    "mro_system.cron.CheckMaintenance",
    "mro_system.cron.ReadCounters",
]

# add request data to the template context processors
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

# Set an extra locale search path for the project
LOCALE_PATHS = (
    os.path.join(SITE_ROOT, '..', 'locale'),
)

# use minified static files, compile_less managment command
# create the minified files
# USAGE:
#   ./manage.py compile_less
USE_MINIFY = True

CRISPY_TEMPLATE_PACK = 'bootstrap'

# path to binary wkhtmltopdf command line utility
WKHTMLTOPDF_CMD = '%s/bin/wkhtmltopdf' % SITE_ROOT

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
