from django.conf.urls.defaults import patterns, url, include
from .resources import UserResource

urlpatterns = patterns('',
    (r'^user/$', include(UserResource().urls)),
)
