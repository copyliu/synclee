from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('api.views',
    url(r'^user/follow/$', 'user_follow', name="ajax_user_follow"),
    url(r'^invite_user/$', 'invite_user', name="ajax_invite_user"),
    url(r'^work/follow/$', 'work_follow', name="ajax_work_follow"),
    url(r'^apply_work/$', 'apply_work', name="ajax_apply_work"),
)
