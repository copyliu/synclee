from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('api.views',
    url(r'^follow_user/$', 'follow_user', name="ajax_follow_user"),
    url(r'^invite_user/$', 'invite_user', name="ajax_invite_user"),
    url(r'^follow_work/$', 'follow_work', name="ajax_follow_work"),
    url(r'^apply_work/$', 'apply_work', name="ajax_apply_work"),
)
