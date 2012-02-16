from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from notification import urls as notification

import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.home', name='home'),
    url(r'^unread$', 'views.unread', name='unread'),
    url(r'^', include('tools.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^works/', include('works.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^notification/', include(notification)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)
