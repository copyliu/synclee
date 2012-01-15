from django.conf.urls.defaults import *

from synclee.notification.views import notices, mark_all_seen, feed_for_user, single, notice_settings, refresh_notices, refresh_pager

urlpatterns = patterns('',
    url(r'^$', notices, name="notification_notices"),
    url(r'^settings/$', notice_settings, name="notification_notice_settings"),
    url(r'^(\d+)/$', single, name="notification_notice"),
    url(r'^feed/$', feed_for_user, name="notification_feed_for_user"),
    url(r'^mark_all_seen/$', mark_all_seen, name="notification_mark_all_seen"),
    url(r'^refresh/$', refresh_notices, name="refresh_notice"),
    url(r'^refresh_pager/$', refresh_pager, name="refresh_pager"),
)
