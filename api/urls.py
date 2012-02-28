from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('api.views',
    url(r'^user/follow/$', 'user_follow', name="ajax_user_follow"),
    url(r'^work/follow/$', 'work_follow', name="ajax_work_follow"),
    url(r'^apply_work/$', 'apply_work', name="ajax_apply_work"),
    url(r'^work/invite/add/$', 'work_invite', name="ajax_work_invite"),
    url(r'^work/invite/accept/$', 'work_invite_accept', name="ajax_work_invite_accept"),
    url(r'^work/invite/reject/$', 'work_invite_reject', name="ajax_work_invite_reject"),
)
