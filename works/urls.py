from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('works.views',
    url(r'^add_work/$', 'add_work', name='add_work'),
    url(r'^show_work/(?P<work_id>\d+)/$', 'show_work', name='show_work'),
    url(r'^write_work/(?P<work_id>\d+)/$', 'write_work', name='write_work'),
    url(r'^edit_work/(?P<work_id>\d+)/$', 'edit_work', name='edit_work'),
    url(r'^show_element/(?P<element_id>\d+)/$', 'show_element', name='show_element'),
    url(r'^apply/$', 'apply_for', name = 'apply_for'),
    url(r'^invite/$', 'invite', name = 'invite'),
    url(r'^follow_work/$', 'follow_work', name = 'follow_work'),
    url(r'^list_works/$', 'list_works', name='list_works'),
    url(r'^work_score/$', 'work_score', name='work_score'),
    url(r'^list_works_history/(?P<work_id>\d+)/$', 'list_works_history', name='list_works_history'),
)
