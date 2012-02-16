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
from django.db.models import Avg

from notification import models as notification

from .models import Work, Element, WorkScore, WorkHistory
from .forms import WorkForm

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from accounts.models import *

#import string, random

PRIVACY_CHOICES = (
        (u'Pub', u'公开'),
        (u'Fri', u'好友可见'),
        (u'Pri', u'私人'),        
    )

@commit_on_success
@login_required  
def add_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            intro = form.cleaned_data['intro']
            category = form.cleaned_data['category']
            isprivate = form.cleaned_data['isprivate']
            work = Work.objects.create(name=name, intro=intro, category=category, isprivate=isprivate, author=request.user)
            #handle cover
            cover = request.FILES.get('cover', '')
            if cover:
                cover.name = str(work.id) + '.' + cover.name.split('.')[-1]
            work.cover = cover
            work.save()
            #
            
        #object_type = ContentType.objects.get(name='work')
        #object_id = new_work.id
        #notification.send([user], "new_work", {"from_user": user, "work":new_work}, sender=user, object_type=object_type, object_id=object_id)
            return HttpResponseRedirect('/works/write_work/%s' % work.id)
        else:
            return TemplateResponse(request, 'works/add_work.html', {'form': form})

    else:
        form = WorkForm()
        return TemplateResponse(request, 'works/add_work.html', {'form': form})



@login_required
def apply_for(request):
    action = request.POST.get('type', '')
    if action == 'apply_for':
        role = request.POST.get('role')
        reason = request.POST.get('reason', '')
        work_id = request.POST.get('work_id', '-1')
        work = Work.objects.get(pk=int(work_id))
        #if len(reason) > 300:
        #    reason = reason[:300]
        invitation = Invitation.objects.filter(work = work, invited = request.user).exclude(invite_status = 'reject').count()
                 
        if invitation > 0:
            return HttpResponse("already_invite")
        else:
            Invitation.objects.create(work = work, invited = request.user,
                                          skill = role, reason = reason,
                                          invite_status = 'goingon')
            return HttpResponse("success")

@csrf_exempt
@login_required
def follow_work(request):
    action = request.POST.get('action')
    work = Work.objects.get(pk=request.POST.get('foid', 0))
    if action == 'fo':
        work.follower.add(request.user)
        notification.send_now([work.author,], "follow_work")
        return HttpResponse("success")
    elif action == 'unfo':
        work.follower.remove(request.user)
        return HttpResponse("success")
    
def show_work(request, work_id):
    work = Work.objects.get(pk=work_id)
    if work.isprivate:
        if not _involved(work, request.user):
            raise Http404("private work")
    
    try:
        elements = Element.objects.filter(work=work)
    except:
        elements = None
    
    followed = (request.user in work.follower.all()) or request.user == work.author
    participated = Invitation.objects.filter(work = work, invite_status = 'accept')
    participated = [i.invited for i in participated]
    history = WorkHistory.objects.filter(work = work)[:10]
    context = {'work': work, 'elements' : elements, 'involved': _involved(work, request.user), 'followed': followed, 'participated':participated, 'history':history}
    
    context['average_score'] = WorkScore.objects.filter(work=work).aggregate(average_score=Avg('score'))['average_score']
    context['score_count'] = WorkScore.objects.filter(work=work).count()
    if not context['average_score']:
        context['average_score'] = 0
    
    if request.user.is_authenticated():
        try:
            context['score'] = WorkScore.objects.get(work = work, user = request.user).score
        except Exception as e:
            context['score'] = 0
        
        print context['score'], "!!!!"
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

def _involved(work, user):
    try:
        if user.id == work.author.id: return True
        if Invitation.objects.filter(work = work, invited = user, invite_status = 'accept').count():
            return True
    except: return False
    return False

@csrf_exempt
@login_required
def write_work(request, work_id):
    if not _involved(Work.objects.get(pk=int(work_id)), request.user):
        raise Http404("no privilege")
    if request.method == 'POST':
        category = request.POST.get('category', '')
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        element = Element.objects.create(work_id=work_id, category=category, title=title, content=content)
        element.save()
        return HttpResponse(element.id)
    else:
        work = Work.objects.get(pk=int(work_id))
        participated = Invitation.objects.filter(work = work, invite_status = 'accept')
        participated = [i.invited for i in participated]
        return TemplateResponse(request, 'works/write_work.html', {'work' : work, 'participated':participated})
    
@csrf_exempt
@login_required
def edit_work(request, work_id):
    if not _involved(Work.objects.get(pk=int(work_id)), request.user):
        raise Http404("no privilege")
    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            work = Work.objects.get(pk=work_id, author=request.user)
            elements = Element.objects.filter(work=work)
            elements.delete()
            
            WorkHistory.objects.create(work = work, user = request.user)
            return HttpResponse('delete_success')
        category = request.POST.get('category', '')
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        element = Element.objects.create(work_id=work_id, category=category, title=title, content=content)
        element.save()
        return HttpResponse(element.id)
    elif request.method == 'GET':
        work = Work.objects.get(pk=int(work_id))
        participated = Invitation.objects.filter(work = work, invite_status = 'accept')
        participated = [i.invited for i in participated]
        elements = Element.objects.filter(work=work)
        return TemplateResponse(request, 'works/edit_work.html', {'work' : work, 'elements' : elements, 'participated':participated})
    
def show_element(request, element_id):
    element = get_object_or_404(Element, pk=element_id)
    if element.work.isprivate:
        if not _involved(element.work, request.user):
            raise Http404("private work")
    
    prev = Element.objects.filter(work=element.work).filter(id__lt=element.id)
    next = Element.objects.filter(work=element.work).filter(id__gt=element.id)
    
    nav = {
        'prev' : prev or False,
        'next' : next or False
    }
    return TemplateResponse(request, 'works/show_element.html', {'element' : element, 'nav' : nav})

def list_works(request):
    works = Work.objects.all()
    #分页
    paginator = Paginator(works, 1)
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1    
    works = paginator.page(page)
    request.session['page'] = page
    
    return TemplateResponse(request, 'works/list_works.html', {'works' : works, 'paginator' : paginator})

def list_works_history(request, work_id):
    work = Work.objects.get(pk=work_id)
    if work.isprivate:
        if not _involved(work, request.user):
            raise Http404("private work")
    history = WorkHistory.objects.filter(work = work)
    
    #分页
    paginator = Paginator(history, 1)
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1
    
    history = paginator.page(page)
    request.session['page'] = page
    
    return TemplateResponse(request, 'works/list_works_history.html', {'history' : history, 'paginator' : paginator})

@login_required
def work_score(request):
    score = int(request.POST.get('score', '0'))
    work_id = request.POST.get('work_id', '-1')
    work = get_object_or_404(Work, pk=int(work_id))
    
    tmp = WorkScore.objects.get_or_create(work = work, user = request.user)[0]
    tmp.score = score
    tmp.save()