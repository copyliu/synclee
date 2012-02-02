# -*- coding: UTF-8 -*-
from django.db.transaction import commit_on_success
from django.core.cache import cache
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from .models import Work, Element
from .forms import WorkForm

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from accounts.skills import int2skill
from accounts.models import *
from django.contrib.auth.decorators import login_required
#import string, random
from django.utils import simplejson

PRIVACY_CHOICES = (
        (u'Pub', u'公开'),
        (u'Fri', u'好友可见'),
        (u'Pri', u'私人'),        
    )

@commit_on_success
#@login_required  
def add_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            intro = form.cleaned_data['intro']
            work = Work.objects.create(name=name, intro=intro, author=request.user)
            #handle cover
            cover = request.FILES.get('cover', '')
            if cover:
                cover.name = str(work.id) + '.' + cover.name.split('.')[-1]
            work.cover = cover
            work.save()
            #uploaded = request.FILES.get('cover', '')
            #catalog_id = request.POST.get('catalog_id')
            
        #object_type = ContentType.objects.get(name='work')
        #object_id = new_work.id
        #notification.send([user], "new_work", {"from_user": user, "work":new_work}, sender=user, object_type=object_type, object_id=object_id)
            return HttpResponseRedirect('/works/write_work/%s' % work.id)
        else:
            return TemplateResponse(request, 'works/add_work.html', {'form': form})

    else:
        form = WorkForm()
        return TemplateResponse(request, 'works/add_work.html', {'form': form})

def show_work(request, work_id):
    work = Work.objects.get(pk=work_id)
    
    if request.method == 'POST' and request.user.is_authenticated():
        type = request.POST.get('type', '')
        
        if type == 'apply':
            try:
                role = request.POST.get('role')
                reason = request.POST.get('reason', '')
                if len(reason) > 300:
                    reason = reason[:300]
                invitation = Invitation.objects.filter(work = work, invited = request.user)
                
                if len(invitation) > 0:
                    invitation = invitation[0]
                    invitation.invite_status = 'goingon'
                    invitation.role = role
                    invitation.reason = reason
                    invitation.save()
                else:
                    Invitation.objects.create(work = work, invited = request.user,
                                              skill = role, reason = reason,
                                              invite_status = 'goingon')
            except Exception as e:
                print e
        return HttpResponse("")
    
    try:
        elements = Element.objects.filter(work=work)
    except:
        elements = None
    
    context = {'work': work, 'elements' : elements}
    
    if request.user.is_authenticated():
        if work.author.id != request.user.id:
            skill = UserSkills.objects.filter(user = request.user)
            skill_list = []
            for i in skill:
                for j in SKILL_CHOICES:
                    if i.skill == j[0]:
                        skill_list.append((i.skill, i.exp, j[1]))
            context['skill_list'] = skill_list
        else:
            context['apply_set'] = Invitation.objects.filter(work = work, invite_status = 'goingon')
            print len(context['apply_set']),"####"
    return TemplateResponse(request, 'works/show_work.html', context)

@csrf_exempt
def write_work(request, work_id):
    if request.method == 'POST':
        category = request.POST.get('category', '')
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        element = Element.objects.create(work_id=work_id, category=category, title=title, content=content)
        element.save()
        return HttpResponse(element.id)
    else:
        work = Work.objects.get(pk=int(work_id))
        return TemplateResponse(request, 'works/write_work.html', {'work' : work})
    
@csrf_exempt
@login_required
def edit_work(request, work_id):
    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            work = Work.objects.get(pk=work_id, author=request.user)
            elements = Element.objects.filter(work=work)
            elements.delete()
            return HttpResponse('delete_success')
        category = request.POST.get('category', '')
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        element = Element.objects.create(work_id=work_id, category=category, title=title, content=content)
        element.save()
        return HttpResponse(element.id)
    elif request.method == 'GET':
        work = Work.objects.get(pk=int(work_id))
        elements = Element.objects.filter(work=work)
        return TemplateResponse(request, 'works/edit_work.html', {'work' : work, 'elements' : elements})
    
def show_element(request, element_id):
    element = get_object_or_404(Element, pk=element_id)
    prev = Element.objects.filter(work=element.work).filter(id__lt=element.id)
    next = Element.objects.filter(work=element.work).filter(id__gt=element.id)
    
    nav = {
        'prev' : prev or False,
        'next' : next or False
    }
    return TemplateResponse(request, 'works/show_element.html', {'element' : element, 'nav' : nav})