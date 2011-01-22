from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from views import *

urlpatterns = patterns('',
    url(r'^(?P<profile_slug>[\w\._-]+)/$', display_profile, name='display_author'),
)
