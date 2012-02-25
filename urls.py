from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from notification import urls as notification
from tastypie.api import Api

import settings
from api.resources import UserResource, WorkResource
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(WorkResource())

handler500 = 'views.server_error'
handler404 = 'views.server_error_404'

urlpatterns = patterns('',
    url(r'^$', 'views.home', name='home'),
    url(r'^', include('tools.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^unread$', 'views.unread', name='unread'),
    url(r'^works/', include('works.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^notification/', include(notification)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)
