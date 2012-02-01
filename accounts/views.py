# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm

from accounts.forms import RegistrationForm, UserProfileForm, GetPasswordForm, ResetPasswordForm
from accounts.models import UserProfiles, AccountTempPassword, Invitation
from works.models import Work, TimeLines
from django.http import Http404, HttpResponseRedirect

from .skills import set_skill, int2skill
import random
from threading import Thread
import datetime
import time

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


def profile(request, username):
    
    user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        type = request.POST.get('type', '')
        if type == 'invite':
            try:
                work_id = request.POST.get('work_id', '-1')
                work = Work.objects.get(pk=int(work_id))
                role = request.POST.get('role')
                reason = request.POST.get('reason', '')
                if len(reason) > 300:
                    reason = reason[:300]
                invitation = Invitation.objects.filter(work = work, invited = user)
                
                if len(invitation) > 0:
                    invitation = invitation[0]
                    invitation.b_from = True
                    invitation.role = role
                    invitation.reason = reason
                    invitation.save()
                else:
                    Invitation.objects.create(work = work, invited = user,
                                              skill = role, reason = reason,
                                              b_from = True, b_to =False)
            except Exception as e:
                print e
        return HttpResponse("")
    
    profile = UserProfiles.objects.get(user=user)
    profile_skill = int2skill(profile.skill)
    work_set = user.work_set.all()
    work_set2 = request.user.work_set.all()
    timeline = TimeLines.objects.filter(user__username=username)
    if user.id == request.user.id:
        pass
    context = {
        'profile':profile, 
        'profile_skill':profile_skill,
        'work_set' : work_set,
        'work_set2' : work_set2,
        'timeline' : timeline
    }
    return TemplateResponse(request, 'accounts/profile.html', context)

@login_required
def settings(request, item):
    profile = UserProfiles.objects.get(pk=request.user.id)
    
    if item == "profile":
        return _set_profile(request, profile)
    elif item == "skill":
        return set_skill(request, profile)
    elif item == "psw":
        return set_psw(request)
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

def set_psw(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
        else: 
            return TemplateResponse(request, 'accounts/setting_psw.html', {'form': form, 'active':'psw'})  
    form = PasswordChangeForm(user = request.user)
    return TemplateResponse(request, 'accounts/setting_psw.html', {'form': form, 'active':'psw'})

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