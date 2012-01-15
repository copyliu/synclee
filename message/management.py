from django.conf import settings
from django.utils.translation import ugettext_noop as _
from django.db.models import signals

if "synclee.notification" in settings.INSTALLED_APPS:
    from synclee.notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("new_message", _("New Message"), _("you get a new message"))
    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"