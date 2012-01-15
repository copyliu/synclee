from django.conf.urls.defaults import *

urlpatterns = patterns('synclee.relationships.views',
    url(r'^$', 'relationship_redirect', name='relationship_list_base'),
    url(r'^(?P<username>[\w-]+)/(?P<status_slug>[\w-]+)/refresh/', 'refresh_relations', name='refresh_relations'),
    url(r'^(?P<username>[\w-]+)/(?:(?P<status_slug>[\w-]+)/)?$', 'relationship_list', name='relationship_list'),
    url(r'^add/(?P<username>[\w-]+)/(?P<status_slug>[\w-]+)/$', 'relationship_handler', {'add': True}, name='relationship_add'),
    url(r'^remove/(?P<username>[\w-]+)/(?P<status_slug>[\w-]+)/$', 'relationship_handler', {'add': False}, name='relationship_remove'),
)
