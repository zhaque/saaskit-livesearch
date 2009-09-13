from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'livesearch.views.searches', name='livesearch_search_homepage'),
    url(r'^(?P<slug>[-\w]+)/$', 'livesearch.views.search', name='livesearch_results'),
)
