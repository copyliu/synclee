# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm

from accounts.forms import RegistrationForm, UserProfileForm, GetPasswordForm, ResetPasswordForm
from accounts.models import *
from works.models import Work, TimeLines
from django.http import Http404, HttpResponseRedirect

import random, datetime, time
from threading import Thread

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data["password"]
            User.objects.create_user(username = username, email = email, password = password)
            
            # django bug, must authenticate before login
            user = authenticate(username = username, password = password)
            login(request, user)
            
            return redirect('/')
    else:
        form = RegistrationForm()

    return TemplateResponse(request, 'accounts/register.html', {'form': form})

@csrf_exempt
def follow(request):
    action = request.POST.get('action')
    user = User.objects.get(pk=request.POST.get('foid'))
    if action == 'fo':
        request.user.relationships.add(user)
        return HttpResponse("success")
    elif action == 'unfo':
        request.user.relationships.remove(user)
        return HttpResponse("success")

@csrf_exempt
def invite(request):
    username = request.POST.get('username', '')
    user = get_object_or_404(User, username=username)
    work_id = request.POST.get('work_id', '-1')
    reason = request.POST.get('reason', '')
    try:
        work = Work.objects.get(pk=int(work_id))
        #中文不能直接截取
#        if len(reason) > 300:
#            reason = reason[:300]
        invitation = Invitation.objects.filter(work = work, invited = user, invite_status = 'noanswer').count()
        invitation = invitation + Invitation.objects.filter(work = work, invited = user, invite_status = 'accept').count()
        invitation = invitation + Invitation.objects.filter(work = work, invited = user, invite_status = 'goingon').count()
        
        if invitation:
            return HttpResponse("already_invite")
        else:
            Invitation.objects.create(work = work, invited = user,
                                      reason = reason,
                                      invite_status = 'noanswer')
    except Exception as e:
        print e
    return HttpResponse('success')

@login_required
def notice(request):
    action = request.POST.get('type', '')
    if action == "invite_accept":
        try:
            id = request.POST.get('id', '-1')
            invitation = Invitation.objects.get(id = int(id))
            if invitation.invited.id == request.user.id:
                invitation.invite_status = 'accept'
                invitation.save()
        except: return HttpResponse("something wrong")
    elif action == "invite_reject":
        try:
            id = request.POST.get('id', '-1')
            invitation = Invitation.objects.get(id = int(id))
            if invitation.invited.id == request.user.id:
                invitation.invite_status = 'reject'
                invitation.save()
        except: return HttpResponse("something wrong")
    elif action == "apply_accept":
        try:
            id = request.POST.get('id', '-1')
            invitation = Invitation.objects.get(id = int(id))
            if invitation.work.author.id == request.user.id:
                invitation.invite_status = 'accept'
                invitation.save()
        except: return HttpResponse("something wrong")
    elif action == "apply_reject":
        try:
            id = request.POST.get('id', '-1')
            invitation = Invitation.objects.get(id = int(id))
            if invitation.work.author.id == request.user.id:
                invitation.invite_status = 'reject'
                invitation.save()
        except: return HttpResponse("something wrong")
    return HttpResponse("success")

def profile(request, username):
    user = get_object_or_404(User, username=username)

    profile = UserProfiles.objects.get(user=user)
    timeline = TimeLines.objects.filter(user__username=username)
    #invited = Invitation.objects.filter(invited=user, invite_status='noanswer')
    joined = Invitation.objects.filter(invited=user, invite_status='accept')
    joined = [i.work for i in joined]
    work_set = user.work_set.all()
    skill = UserSkills.objects.filter(user = user)
    skill_list = []
    for i in skill:
        for j in SKILL_CHOICES:
            if i.skill == j[0]:
                skill_list.append((i.skill, i.exp, j[1]))
            
    # TODO: context中加入skill
    context = {
        'profile' : profile, 
        'timeline' : timeline,
        #'invited' : invited,
        'joined' : joined,
        'followed' : user.follow.all(),
        'skill_list' : skill_list,
    }
    
    if request.user.is_authenticated():
        if request.user.id == profile.user_id:
            context['invitation'] = Invitation.objects.filter(invited = request.user, invite_status = 'noanswer')
    
    return TemplateResponse(request, 'accounts/profile.html', context)

@login_required
def settings(request, item):
    profile = UserProfiles.objects.get(pk=request.user.id)
    
    if item == "profile":
        return _set_profile(request, profile)
    elif item == "skill":
        return _set_skill(request, profile)
    elif item == "psw":
        return _set_psw(request)
    else:
        raise Http404("no setting")
            
def _set_profile(request, profile):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile.true_name = form.cleaned_data['true_name']
            profile.email = form.cleaned_data['email']
            profile.location = form.cleaned_data['location']
            profile.intro = form.cleaned_data['intro']
            if request.FILES.get('avatar', ''):
                profile.avatar = request.FILES.get('avatar', '')
                profile.avatar.name = str(request.user.id)+'.'+profile.avatar.name.split('.')[-1]
            profile.save()
            return HttpResponseRedirect('/accounts/settings/profile/')
        else:
            return TemplateResponse(request, 'accounts/setting_profile.html', {'profile':profile, 'form': form, 'active':'profile'})
    else:
        form = UserProfileForm()
        return TemplateResponse(request, 'accounts/setting_profile.html', {'profile':profile, 'form': form, 'active':'profile'})

def _set_psw(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
        else: 
            return TemplateResponse(request, 'accounts/setting_psw.html', {'form': form, 'active':'psw'})  
    form = PasswordChangeForm(user = request.user)
    return TemplateResponse(request, 'accounts/setting_psw.html', {'form': form, 'active':'psw'})

def _set_skill(request, profile):
    skill_list = {}
    for skill in SKILL_CHOICES:
        skill_list[skill[0]] = (skill[1], "")
    
    for i in UserSkills.objects.filter(user = request.user):
        skill_list[i.skill] = (skill_list[i.skill][0], "checked")
    
    if request.method == 'POST':
        for i, _ in request.POST.items():
            if i.startswith("skill_"):
                i = i[6:]
                cnt = UserSkills.objects.filter(user = request.user, skill = i).count()
                if cnt == 0:
                     UserSkills.objects.create(user = request.user, skill = i, exp = 0, today_exp = 0)
                skill_list[i] = (skill_list[i][0], "checked")
        # TODO: 去掉勾选
                 
    return TemplateResponse(request, 'accounts/setting_skill.html', {'skill_list': skill_list, 'active': "skill"})

def reset_psw(request):
    if request.method == 'POST':
        form = GetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email = form.cleaned_data['email'])
            tmp_psw = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in xrange(20)])
            
            AccountTempPassword.objects.filter(user = user).delete()
            tmp = AccountTempPassword(user = user, tmp_psw = tmp_psw)
            tmp.save()
            
            #发送邮件
            print tmp_psw
            url = r"http://127.0.0.1:8000/accounts/reset/confirm/%s/" % tmp_psw
            tr = Thread(target = user.email_user,
                        args = ("重置密码", '请点击 %s' % url))
            tr.start()
            
            return render_to_response('accounts/reset_psw_sended.html', {})
        else:
            return TemplateResponse(request, 'accounts/reset_psw.html', {'form': form}) 
    form = GetPasswordForm()
    return TemplateResponse(request, 'accounts/reset_psw.html', {'form': form})
    

def reset_psw_confirm(request, tmp_psw):
    tmp_user = get_object_or_404(AccountTempPassword, tmp_psw = tmp_psw)
    delta = time.mktime(datetime.datetime.now().timetuple()) - time.mktime(tmp_user.datetime.timetuple())
    
    if delta > 60 * 60:
        tmp_user.delete()
        raise Http404("临时密码过期")
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            tmp_user.user.set_password(password)
            tmp_user.user.save()
            tmp_user.delete()
            
            return render_to_response('accounts/reset_psw_done.html', {})
        else:
            return TemplateResponse(request, 'accounts/reset_psw_confirm.html', {'form': form})
    form = ResetPasswordForm()
    return TemplateResponse(request, 'accounts/reset_psw_confirm.html', {'form': form})