from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^about/', direct_to_template, {"template": "about.html.django"}, name="about"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^author/', include('profile.urls')),
    url(r'^toggle-mobile/', toggle_mobile, name='toggle_mobile'),
    url(r'^favicon.ico', favicon_redirect, {}, name="favicon_redirect"),
    url(r'^sitemap.xml', sitemap, {}, name="sitemap"),
    url(r'', include('strands_core.urls')),    
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )
