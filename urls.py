# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings
from settings import SITE_DIR
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#TODO:要禁止关键字注册用户名

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('synclee.registration.backends.default.urls')),
    (r'^club/', include('synclee.club.urls')),
    (r'^work/', include('synclee.work.urls')),
    (r'^friends/', include('synclee.relationships.urls')),
    (r'^message/', include('synclee.message.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^notes/', include('synclee.notification.urls')),
    (r'^tab/', include('synclee.tab.urls')),
    (r'^tweet/',include('synclee.tweet.urls')),
    (r'^board/',include('synclee.billboard.urls')),
    (r'^', include('synclee.general.urls')),
    (r'^', include('synclee.search.urls')),
    (r'^', include('synclee.profiles.urls')),
    
    (r'^style/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"])+'/static/style'}),
    (r'^script/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"])+'/static/script'}),
    (r'^rc/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"])+'/static/rc'}),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"])+'/uploads'}),
)
