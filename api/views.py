# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, render_to_response, HttpResponse

from works.models import Work
from accounts.models import Invitation
from notification import models as notification
from tools import SkillManager
import json

@csrf_exempt
def user_follow(request):
    action = request.GET.get('action')
    user = User.objects.get(pk=request.GET.get('uid'))
    if action == 'follow':
        request.user.relationships.add(user)
        notification.send([user,], "follow_user", {"notice_label": "follow_user", "user": request.user})
    elif action == 'unfollow':
        request.user.relationships.remove(user)
    
    return HttpResponse(json.dumps({'action': action, 'username': user.username}))

@csrf_exempt
def work_follow(request):
    action = request.GET.get('action')
    work = Work.objects.get(pk=request.GET.get('wid', 0))
    if action == 'follow':
        work.follower.add(request.user)
        notification.send([work.author,], "follow_work", {"notice_label": "follow_work", "work": work, "user": request.user})
    elif action == 'unfollow':
        work.follower.remove(request.user)
        
    return HttpResponse(json.dumps({'action': action, 'work': work.name}))

@csrf_exempt
def work_invite(request):
    uid = request.POST.get('uid', '')
    user = get_object_or_404(User, pk=uid)
    work_id = request.POST.get('work_id', '-1')
    work = Work.objects.get(pk=int(work_id))
    role = request.POST.get('role', '-1')
    
    if work.author != request.user or (not role in ["image", "word", "other"]):
        raise BaseException("sth wrong")
    
    reason = request.POST.get('reason', '')
    print uid, work_id, reason, role
    try:
        invitation = Invitation.objects.filter(work = work, invited = user).exclude(invite_status = 'reject').count()
        print invitation
        if invitation:
            raise BaseException("invited")
        else:
            invitation = Invitation.objects.create(work = work, invited = user,
                                      reason = reason,
                                      invite_status = 'noanswer')
            notification.send([user,], "invite_user", {"notice_label": "invite_user", "work": work, "user": request.user, "role":role, "invited": user, "id":invitation.id})
    except Exception as e:
        print e
    return HttpResponse("done")

@csrf_exempt
def work_invite_accept(request):
    invitation = Invitation.objects.get(pk=int(request.GET.get('id')))
    if invitation.invited == request.user and invitation.invite_status == "noanswer":
        invitation.invite_status = "accept"
        invitation.save()
        SkillManager.addexp(request.user, invitation.work.category, 5)
    
    return HttpResponse("done")

@csrf_exempt
def work_invite_reject(request):
    invitation = Invitation.objects.get(pk=int(request.GET.get('id')))
    if invitation.invited == request.user and invitation.invite_status == "noanswer":
        invitation.invite_status = "reject"
        invitation.save()
    
    return HttpResponse("done")

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