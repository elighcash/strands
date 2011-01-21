from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from views import *
from feeds import *

feeds = {'latest.xml': latest_knots,
        'author.xml': author_feed,
        'all.xml': all_knots}

urlpatterns = patterns('',
    #index url
    url(r'^$', index, name="home"),


    #misc urls
    url(r'^toggle-mobile/', toggle_mobile, name='toggle_mobile'),
    url(r'^feeds/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="feed"),
    
    #strands main urls
    url(r'^strands/\#(?P<a>[\w]+)$', tapestry, name='tapestry_parameter'),                  #these two are here for reversal purposes mostly
    url(r'^strands/\#(?P<a>[\w]+)\&(?P<b>[\w]+)$', tapestry, name='tapestry_parameters'),
    url(r'^strands/$', tapestry, name='tapestry'),
    url(r'^author/(?P<author_username>[\w\._-]+)/$', display_author, name='display_author'),
    url(r'^knot/(?P<knot_slug>[\w\._-]+)/$', display_knot, name='display_knot'),
    
    #strands short urls
    url(r'^(?P<knot_short>[a-zA-Z0-9]+)/$', display_knot_short, name='display_knot_short'),
)
