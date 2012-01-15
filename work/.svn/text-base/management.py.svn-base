from django.conf import settings
from django.utils.translation import ugettext_noop as _
from django.db.models import signals

if "synclee.notification" in settings.INSTALLED_APPS:
    from synclee.notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("work_apply", _("Work Application Received"), _("you have received a work application"))
        notification.create_notice_type("work_invite", _("Work Invitation Received"), _("you have received a work invitation"))
        notification.create_notice_type("work_accept", _("Work Acceptance Received"), _("a work invitation you sent has been accepted"))
        notification.create_notice_type("work_deny", _("Work Deny Received"), _("a work invitation you sent has been denied"))
        notification.create_notice_type("new_work", _("New Work"), _("a work has been found"))
        notification.create_notice_type("edit_work", _("Edit Work"), _("a work has been found"))
        notification.create_notice_type("new_text", _("New Text"), _("a work has been found"))
        notification.create_notice_type("edit_text", _("Edit Text"), _("a work has been found"))
        notification.create_notice_type("new_gallery", _("New Gallery"), _("a work has been found"))
        notification.create_notice_type("edit_gallery", _("Edit Gallery"), _("a work has been found"))
        notification.create_notice_type("sync_text", _("Sync Text"), _("a work has been found"))
        notification.create_notice_type("sync_gallery", _("Sync Gallery"), _("a work has been found"))
        notification.create_notice_type("new_reply", _("New Reply"), _("a work has been found"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"