from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('works.views',
    url(r'^add_work/$', 'add_work', name='add_work'),)
