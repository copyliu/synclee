from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('api.views',
    url(r'^user/follow/$', 'user_follow', name="ajax_follow_user"),
    url(r'^invite_user/$', 'invite_user', name="ajax_invite_user"),
    url(r'^work/follow/$', 'follow_work', name="ajax_follow_work"),
    url(r'^apply_work/$', 'apply_work', name="ajax_apply_work"),
)
