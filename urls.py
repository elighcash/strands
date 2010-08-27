from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^about/', direct_to_template, {"template": "about.django.html"}, name="about"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('strands.urls')),    
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )
