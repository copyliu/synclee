from django.db import transaction, models
from accounts.models import UserSkills
from works.models import Work

@transaction.commit_on_success
def addexp(user, category, x):
    tem = UserSkills.objects.get(user = user, skill = category)
    tem.exp += x
    tem.save()

def exp_add_work(sender = None, instance = None, created = False, **kwargs):
    if created:
        addexp(instance.author, instance.category, 10)
models.signals.post_save.connect(exp_add_work, sender = Work)