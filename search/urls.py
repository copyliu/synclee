from django.conf.urls.defaults import *

urlpatterns = patterns('synclee.search.views',
    url(r'^search/refresh/$', 'refresh_search', name='ReSearch'),
    url(r'^search/$', 'search', name='Search'),
)