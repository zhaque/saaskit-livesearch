from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'livesearch.views.searches', name='livesearch_search_homepage'),
    url(r'^results$', 'livesearch.views.results', name='livesearch_all_results'),
    url(r'^images$', 'livesearch.views.image_results', name='livesearch_image_results'),
    url(r'^videos$', 'livesearch.views.video_results', name='livesearch_video_results'),
    url(r'^news$', 'livesearch.views.news_results', name='livesearch_news_results'),
    url(r'^web$', 'livesearch.views.web_results', name='livesearch_web_results'),
    url(r'^twitter$', 'livesearch.views.twitter_results', name='livesearch_twitter_results'),
)
