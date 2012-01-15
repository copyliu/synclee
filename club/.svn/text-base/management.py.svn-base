from django.conf import settings
from django.utils.translation import ugettext_noop as _
from django.db.models import signals

if "synclee.notification" in settings.INSTALLED_APPS:
    from synclee.notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("club_apply", _("Club Application Received"), _("you have received a club application"))
        notification.create_notice_type("club_invite", _("Club Invitation Received"), _("you have received a club invitation"))
        notification.create_notice_type("club_accept", _("Club Acceptance Received"), _("a club invitation you sent has been accepted"))
        notification.create_notice_type("club_deny", _("Club Deny Received"), _("a club invitation you sent has been denied"))
        notification.create_notice_type("new_club", _("New Club"), _("a work has been found"))
        notification.create_notice_type("new_club_text", _("New Text"), _("a work has been found"))
        notification.create_notice_type("new_club_gallery", _("New Gallery"), _("a work has been found"))
        notification.create_notice_type("new_project", _("New Project"), _("a work has been found"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"