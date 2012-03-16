from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('api.views',
    url(r'^user/follow/$', 'user_follow', name="ajax_user_follow"),
    url(r'^work/follow/$', 'work_follow', name="ajax_work_follow"),
    url(r'^apply_work/$', 'apply_work', name="ajax_apply_work"),
    url(r'^work/invite/add/$', 'user_invite', name="ajax_user_invite"),
    url(r'^work/invite/manage/$', 'user_invite_manage', name="ajax_user_invite_manage"),
    url(r'^work/apply/add/$', 'user_apply', name="ajax_user_apply"),
    url(r'^work/quit/$', 'user_quit', name="ajax_user_quit"),
    url(r'^work/grade/$', 'work_grade', name="ajax_work_grade"),
    url(r'^work/element/(?P<work_id>\d+)/(?P<element_id>\d+)/$', 'get_element', name="ajax_get_element")
)
