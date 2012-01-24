# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.shortcuts import redirect #, HttpResponse

from accounts.forms import RegistrationForm, UserProfileForm
from accounts.models import UserProfiles
from django.http import Http404, HttpResponseRedirect

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
    if len(profile) == 0: #初始化默认profile
        profile = UserProfiles(user = user)
        profile.save()
    elif len(profile) > 1:
        raise Http404("something wrong with the username")
    else:
        profile = profile[0]
    return profile

def profile(request, user = None):
    if user is None or user == '': #访问/accounts/profile/
        if request.user.is_authenticated():
            user = request.user
        else:
            raise Http404("Login is required")
    else: #访问/accounts/profile/(用户名)/
        print user
        try:
            user = User.objects.get(username = user)
        except Exception as ex:
            raise Http404(type(ex))  #fix later 用户不存在

    return TemplateResponse(request, 'accounts/profile.html', {'profile':user2profile(user)})

#login required
def settings(request, item):
    if item == "profile":
        if not request.user.is_authenticated():
            raise Http404("Login is required")
        profile = user2profile(request.user)

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
        if not request.user.is_authenticated():
            raise Http404("Login is required")
        profile = user2profile(request.user)
        #TODO
    else:
        raise Http404("no setting")
            
