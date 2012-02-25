# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from notification import models as notification

@csrf_exempt
def follow(request):
    action = request.POST.get('action')
    user = User.objects.get(pk=request.POST.get('foid'))
    if action == 'fo':
        request.user.relationships.add(user)
        notification.send([user,], "follow_user", {"notice_label": "follow_user", "user": request.user})
        return HttpResponse("success")
    elif action == 'unfo':
        request.user.relationships.remove(user)
        return HttpResponse("success")