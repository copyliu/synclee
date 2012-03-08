# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from works.models import Work, WorkScore
from accounts.models import Invitation, SKILL_CHOICES_MAP
from notification import models as notification
from tools import SkillManager
import json

@csrf_exempt
@login_required
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
@login_required
def work_follow(request):
    action = request.GET.get('action')
    work = Work.objects.get(pk=request.GET.get('wid', 0))
    if action == 'follow':
        work.follower.add(request.user)
        notification.send([work.author,], "follow_work", {"notice_label": "follow_work", "work": work, "user": request.user})
    elif action == 'unfollow':
        work.follower.remove(request.user)
        
    return HttpResponse(json.dumps({'action': action, 'work': work.name}))

def _my_assert(ck, msg):
    if ck: return None
    return HttpResponse(json.dumps({'state': 'error',
                                        'error': msg}))

@csrf_exempt
@login_required
def user_invite(request):
    uid = request.POST.get('uid', '')
    user = get_object_or_404(User, pk=uid)
    work_id = request.POST.get('work_id', '-1')
    work = Work.objects.get(pk=int(work_id))
    role = request.POST.get('role', '-1')
    
    tem = _my_assert(work.author == request.user, 'no pri')
    if tem : return tem
    tem = _my_assert(role in ["image", "word", "other"], 'wrong role')
    if tem : return tem
    
    reason = request.POST.get('reason', '')
    
    invitation = Invitation.objects.filter(work = work, invited = user).exclude(invite_status = 'reject').count()
    tem = _my_assert(invitation == 0, 'applyed or invited')
    if tem : return tem
    
    invitation = Invitation.objects.create(work= work, invited= user, role = role,
                                      reason = reason, invite_status = 'noanswer')
    notice = notification.send([user,], "invite_user", {"notice_label": "invite_user", "work": work, "message": reason, "user": request.user, "role":SKILL_CHOICES_MAP[role], "id":invitation.id})
    invitation.notice = notice  
    invitation.save()
    return HttpResponse(json.dumps({'state': 'done',}))

@csrf_exempt
@login_required
def user_apply(request):
    work = Work.objects.get(pk=int(request.POST.get('uid', '-1')))
    role = request.POST.get('role', '-1')
    
    tem = _my_assert(work.author != request.user, 'no pri')
    if tem : return tem
    tem = _my_assert(role in ["image", "word", "other"], 'wrong role')
    if tem : return tem
    
    reason = request.POST.get('reason', '')
    
    invitation = Invitation.objects.filter(work = work, invited = request.user).exclude(invite_status = 'reject').count()
    tem = _my_assert(invitation == 0, 'applyed or invited')
    if tem : return tem
    
    invitation = Invitation.objects.create(work= work, invited= request.user, role = role,
                                      reason = reason, invite_status = 'noanswer')
    notice = notification.send([work.author,], "apply_work", {"notice_label": "apply_work", "work": work, "message": reason, "user": request.user, "role":SKILL_CHOICES_MAP[role], "id":invitation.id})
    invitation.notice = notice  
    invitation.save()
    return HttpResponse(json.dumps({'state': 'done',}))

@csrf_exempt
@login_required
def user_invite_manage(request):
    invitation = Invitation.objects.get(pk=int(request.GET.get('id', '0')))
        
    action = request.GET.get('action', '')
    tem = _my_assert(action in ['accept', 'reject'], 'wrong action')
    if tem : return tem
    
    direction = request.GET.get('direction', '')
    tem = _my_assert(direction in ['apply', 'invite'], 'wrong direction')
    if tem : return tem
    
    tem = _my_assert((direction == 'invite' and invitation.invited == request.user) or (direction == 'apply' and invitation.work.author == request.user), 'no pri')
    if tem : return tem
    tem = _my_assert(invitation.invite_status == "noanswer", 'answered')
    if tem : return tem
        
    invitation.invite_status = action
    invitation.save()
    if action == 'accept':
        SkillManager.addexp(invitation.invited, invitation.work.category, 5)
        
    return HttpResponse(json.dumps({'state': 'done',}))

@csrf_exempt
@login_required
def user_quit(request):
    user = User.objects.get(pk=int(request.GET.get('uid', '-1')))
    work = Work.objects.get(pk=int(request.GET.get('wid', '-1')))
    invitation = Invitation.objects.get(work = work, invited = user, invite_status = "accept")
    
    tem = _my_assert(user == request.user or request.user == work.author, 'no pri')
    if tem : return tem
        
    invitation.invite_status = "reject"
    invitation.save()
    SkillManager.addexp(invitation.invited, invitation.work.category, -5)
        
    return HttpResponse(json.dumps({'state': 'done',}))


@csrf_exempt
@login_required
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

@csrf_exempt
@login_required
def work_grade(request):
    score = int(request.GET.get('score', '0'))
    tem = _my_assert(score, 'wrong score')
    if tem : return tem
    
    work_id = request.GET.get('uid', '-1')
    work = get_object_or_404(Work, pk=int(work_id))
    
    tmp = WorkScore.objects.get_or_create(work = work, user = request.user)[0]
    tmp.score = score
    tmp.save()
    
    average_score = WorkScore.objects.filter(work=work).aggregate(average_score=Avg('score'))['average_score'] or 0
    score_count = WorkScore.objects.filter(work=work).count()
    return HttpResponse(json.dumps({'state': 'done', 'average_score': average_score, 'score_count': score_count}))