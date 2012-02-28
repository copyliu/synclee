from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('api.views',
    url(r'^user/follow/$', 'user_follow', name="ajax_user_follow"),
    url(r'^work/follow/$', 'work_follow', name="ajax_work_follow"),
    url(r'^apply_work/$', 'apply_work', name="ajax_apply_work"),
    url(r'^work/invite/add/$', 'user_invite', name="ajax_user_invite"),
    url(r'^work/invite/accept/$', 'user_invite_accept', name="ajax_user_invite_accept"),
    url(r'^work/invite/reject/$', 'user_invite_reject', name="ajax_user_invite_reject"),
)
