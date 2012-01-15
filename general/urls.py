from django.conf.urls.defaults import *

urlpatterns = patterns('synclee.general.views',
    url(r'^about/$', 'about', name='About'),
    url(r'^help/$', 'help', name='Help'),
)