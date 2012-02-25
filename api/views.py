# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, render_to_response, HttpResponse

from notification import models as notification
from works.models import Work
from accounts.models import Invitation

import json

@csrf_exempt
def follow_user(request):
    action = request.POST.get('action')
    user = User.objects.get(pk=request.POST.get('uid'))
    if action == 'follow':
        request.user.relationships.add(user)
        #notification.send([user,], "follow_user", {"notice_label": "follow_user", "user": request.user})
    elif action == 'unfollow':
        request.user.relationships.remove(user)
    
    return HttpResponse(json.dumps({'action': action, 'username': user.username}))

@csrf_exempt
def invite_user(request):
    uid = request.POST.get('uid', '')
    user = get_object_or_404(User, pk=uid)
    work_id = request.POST.get('work_id', '-1')
    role = request.POST.get('role', '-1')
    reason = request.POST.get('reason', '')
    try:
        work = Work.objects.get(pk=int(work_id))
        invitation = Invitation.objects.filter(work = work, invited = user).exclude(invite_status = 'reject').count()
        
        if invitation:
            return HttpResponse("already_invite")
        else:
            invitation = Invitation.objects.create(work = work, invited = user,
                                      reason = reason,
                                      invite_status = 'noanswer')
            notification.send([user,], "invite_work", {"notice_label": "invite_user", "work": work, "user": request.user, "role":role, "invited": user})
    except Exception as e:
        print e
    return HttpResponse(json.dumps({'username': user.username}))

@csrf_exempt
def follow_work(request):
    action = request.POST.get('action')
    work = Work.objects.get(pk=request.POST.get('foid', 0))
    if action == 'fo':
        work.follower.add(request.user)
        notification.send([work.author,], "follow_work", {"notice_label": "follow_work", "work": work, "user": request.user})
        return HttpResponse("success")
    elif action == 'unfo':
        work.follower.remove(request.user)
        
    return HttpResponse("success")

@csrf_exempt
def apply_work(request):
    action = request.POST.get('type', '')
    if action == 'apply_for':
        role = request.POST.get('role')
        reason = request.POST.get('reason', '')
        work_id = request.POST.get('work_id', '-1')
        work = Work.objects.get(pk=int(work_id))
        invitation = Invitation.objects.filter(work = work, invited = request.user).exclude(invite_status = 'reject').count()
                 
        if invitation > 0:
            return HttpResponse("already_invite")
        else:
            invitation = Invitation.objects.create(work = work, invited = request.user,
                                          skill = role, reason = reason,
                                          invite_status = 'goingon')
            notification.send([work.author,], "apply_work", {"notice_label": "apply_work", "work": work, "user": request.user, "role":role})
            return HttpResponse("success")