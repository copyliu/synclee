# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("follow_work", u"你的企划被关注了", u"")
        notification.create_notice_type("apply_work", u"有人申请加入你的企划", u"")
        notification.create_notice_type("invite_work", u"你被邀请加入一个企划", u"")
        notification.create_notice_type("follow_user", u"有人关注了你", u"")
        
    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
