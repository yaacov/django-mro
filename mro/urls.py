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
    url(r'^equipment/', include('mro_equipment.urls')),
    url(r'^order/', include('mro_order.urls')),

)

# breadcrumbs translation guide
breadcrumbs = (
    _('contact'),
    _('warehouse'),
    _('order'),
)