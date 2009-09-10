from django.conf.urls.defaults import *
from django.conf import settings

#from search.views import searches, results, image_results, video_results, search_admin

urlpatterns = patterns('',
    url(r'^$', 'livesearch.views.searches', name='search_homepage'),
    url(r'^results$', 'livesearch.views.results', name='web_results'),
    url(r'^images$', 'livesearch.views.image_results', name='image_results'),
    url(r'^videos$', 'livesearch.views.video_results', name='video_results'),
    url(r'^twitter$', 'livesearch.views.twitter_results', name='twitter_results'),
    url(r'^admin$', 'livesearch.views.search_admin', name='search_administartion'),
)
