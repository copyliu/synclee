# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.shortcuts import redirect #, HttpResponse
from django.contrib.auth.decorators import login_required

from accounts.forms import RegistrationForm, UserProfileForm
from accounts.models import UserProfiles
from django.http import Http404, HttpResponseRedirect

from accounts.skill import set_skill, int2skill

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

def user2profile(user):
    profile = user.profile.all()
    if len(profile) != 1:
        raise Http404("something wrong with the username")
    else:
        profile = profile[0]
    return profile

def profile(request, user = None):
    if not user: #访问/accounts/profile/
        if request.user.is_authenticated():
            user = request.user
        else:
            raise Http404("Login is required")
    else: #访问/accounts/profile/(用户名)/
        try:
            user = User.objects.get(username = user)
        except Exception as ex:
            raise Http404(type(ex))  #fix later 用户不存在
    
    profile = user2profile(user)
    profile_skill = int2skill(profile.skill)
    return TemplateResponse(request, 'accounts/profile.html', {'profile':profile, 'profile_skill':profile_skill})

@login_required
def settings(request, item):
    profile = user2profile(request.user)
    
    if item == "profile":
        if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                profile.true_name = form.cleaned_data['true_name']
                profile.email = form.cleaned_data['email']
                profile.location = form.cleaned_data['location']
                profile.intro = form.cleaned_data['intro']
                profile.save()
                return HttpResponseRedirect('/accounts/settings/profile/')
            else:
                return TemplateResponse(request, 'accounts/setting_profile.html', {'profile':profile, 'form': form, 'active':item})
        else:
            form = UserProfileForm()
            return TemplateResponse(request, 'accounts/setting_profile.html', {'profile':profile, 'form': form, 'active':item})
    elif item == "skill":
        return set_skill(request, profile)
    else:
        raise Http404("no setting")
            
