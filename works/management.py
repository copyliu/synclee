# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("follow_work", u"有人关注了你的企划", _("you have received an invitation"))
        notification.create_notice_type("follow_user", u"有人关注了你", _("an invitation you sent has been accepted"))
        
    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
