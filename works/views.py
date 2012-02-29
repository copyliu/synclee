# -*- coding: UTF-8 -*-
from django.db.models import Avg
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
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from notification import models as notification
from tools import SkillManager

from .models import Work, Element, WorkScore, WorkHistory
from .forms import WorkForm
from accounts.models import Invitation, Skill

#import string, random

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
                cover.name = 'cover.' + cover.name.split('.')[-1]
            work.cover = cover
            work.save()
            return HttpResponseRedirect('/works/write_work/%s' % work.id)
        else:
            return TemplateResponse(request, 'works/add_work.html', {'form': form})

    else:
        form = WorkForm()
        return TemplateResponse(request, 'works/add_work.html', {'form': form})

    
def show_work(request, work_id):
    work = Work.objects.get(pk=work_id)
    if work.isprivate:
        if not _involved(work, request.user):
            raise Http404("private work")
    
    try:
        elements = Element.objects.filter(work=work)
    except:
        elements = None
    
    participated = Invitation.objects.filter(work = work, invite_status = 'accept')
    participated = [i.invited for i in participated]
    followed = (request.user in work.follower.all()) or request.user == work.author
    history = WorkHistory.objects.filter(work = work)[:10]
    context = {'work': work, 'elements' : elements, 'involved': _involved(work, request.user), 'followed': followed, 'history':history, 'participated':participated}
    
    context['average_score'] = WorkScore.objects.filter(work=work).aggregate(average_score=Avg('score'))['average_score'] or 0
    context['score_count'] = WorkScore.objects.filter(work=work).count()

    
    if request.user.is_authenticated():
        try:
            context['score'] = WorkScore.objects.get(work = work, user = request.user).score
        except Exception as e:
            context['score'] = 0
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

def work_rank(request):
    works = Work.objects.all()
    works = filter(lambda work: WorkScore.objects.filter(work=work).count() > 1, works)
    works = sorted(works, key = lambda work: WorkScore.objects.filter(work=work).aggregate(average_score=Avg('score'))['average_score'] or 0, reverse = True)
    for i in works:
        print i.aver_score()
    #分页
    paginator = Paginator(works, 1)
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1
    works = paginator.page(page)
    #print page,"+++",works.object_list[0].aver_score()
    request.session['page'] = page
    
    return TemplateResponse(request, 'works/work_rank.html', {'works' : works, 'paginator' : paginator})

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
