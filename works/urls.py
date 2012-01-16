from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('works.views',
    url(r'^add_work/$', 'add_work', name='add_work'),
    url(r'^write_work/(?P<work_id>\d+)/$', 'write_work', name='write_work'),
)
