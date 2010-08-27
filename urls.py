from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'strands.views.index', name="home"),
    url(r'^about/', direct_to_template, {"template": "about.django.html"}, name="about"),
    url(r'^admin/', include(admin.site.urls)),
    
    #strands/knots
    url(r'^strands/$', 'strands.views.tapestry', name='tapestry'),
    url(r'^strands/(?P<strand_a_slug>[\w\._-]+)/$', 'strands.views.display_strand', name='display_strand_by_a'),
    url(r'^strands/(?P<strand_a_slug>[\w\._-]+)/(?P<strand_b_slug>[\w\._-]+)/$', 'strands.views.display_strand', name='display_strand_by_a_b'),
    url(r'^author/(?P<author_username>[\w\._-]+)/$', 'strands.views.display_by_author', name='display_by_author'),
    url(r'^author/(?P<author_username>[\w\._-]+)/(?P<order>[\w\._-]+)$', 'strands.views.display_by_author', name='display_by_author_order'),
    url(r'^knot/(?P<knot_slug>[\w\._-]+)/$', 'strands.views.display_knot', name='display_knot'),
    #url(r'^date/(?P<date_slug>[\w\._-]+)/$', 'strands.views.display_by_date', name='display_by_date'),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )
