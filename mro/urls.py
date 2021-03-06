from django.conf.urls import patterns, include, url
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mro_theme.views.home', name='home'),
    # url(r'^mro/', include('mro.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# serve the static files
# FIXME: wsgi-servers need extra settings to serve the static files
#   after the extra settings are done in the wsgi-server
#   remove this urlpatterns
#urlpatterns += patterns('',
#    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#        'document_root': settings.STATIC_ROOT,
#    }),
#)

# serve the media files 
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

# applications
urlpatterns += patterns('',
    url(r'^contact/', include('mro_contact.urls')),
    url(r'^warehouse/', include('mro_warehouse.urls')),
    url(r'^equipment/', include('mro_system.urls')),
#    url(r'^systemtype/', include('mro_system_type.urls')),
    url(r'^order/', include('mro_order.urls')),
    url(r'^report/', include('mro_report.urls')),
    url(r'^contract/', include('mro_contract.urls')),
)

# breadcrumbs translation guide
breadcrumbs = (
    _('contact'),
    _('warehouse'),
    _('system'),
#    _('systemtype'),
    _('order'),
    _('report'),
)
