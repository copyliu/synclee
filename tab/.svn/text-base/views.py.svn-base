from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from synclee.club.models import *
from synclee.relationships.models import *
from synclee.profiles.models import UserProfiles, ShareWork
from synclee.tab.models import SubTabClass, TabClass
from synclee.work.models import Work, Membership

@login_required
def showTab(request, slug_name):
    user = request.user
    context = {}
    context['user_profile'] = user.get_profile()
    context['user'] = user
    tabs = TabClass.objects.filter(tab_model_name=slug_name)
    context['tabs'] = tabs
    return render_to_response('tab/show_tab.shtml', context)

@login_required
def showObject(request, slug_name):
    user = request.user
    context = {}
    context['user_profile'] = user.get_profile
    context['user'] = user
    
    tabs = TabClass.objects.filter(tab_model_name=slug_name)
    
    tablist = request.GET.get('tab').split(' ')
    
    #Get Progress with tag1&tag2&tag3&```
    if slug_name == 'work':
        result = Work.objects.all()
    if slug_name == 'project':
        result = Project.objects.all()
    #if slug_name == 'party':
    #    result = Party.objects.all()
    if slug_name == 'profiles':
        result = UserProfiles.objects.all()
    for tab in tablist:
        the_tab = SubTabClass.objects.get(sub_name=tab)
        if slug_name == 'work':
            result = result.filter(tab=the_tab)
        if slug_name == 'profiles':
            result = result.filter(ability=the_tab)
        
    context['result'] = result
    context['slug_name'] = slug_name
    context['tablist'] = tablist
  
    rest_tabs = TabClass.objects.filter(tab_model_name=slug_name)
    
    for tab in tablist:
        the_tab = SubTabClass.objects.get(sub_name=tab)
        rest_tabs = rest_tabs.exclude(pk=the_tab.parent_tab.id)
    context['rest_tabs'] = rest_tabs
    context['request'] = request
    
    return render_to_response('tab/show_object.shtml', context)
    

