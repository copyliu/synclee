# -*- coding: UTF-8 -*-
from django.core.cache import cache

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from synclee.chapter.models import *
from synclee.club.models import *
from synclee.relationships.models import *
from synclee.profiles.models import UserProfiles, ShareWork
from synclee.tab.models import SubTabClass, TabClass
from synclee.work.models import *
from synclee.notification import models as notification
from synclee.relationships.models import RelationshipStatus
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from synclee.billboard.models import Board
from synclee.recommand.models import Recommand

from django.core.paginator import Paginator, InvalidPage, EmptyPage

import string
from django.utils import simplejson
import random

PRIVACY_CHOICES = (
        (u'Pub', u'公开'),
        (u'Fri', u'好友可见'),
        (u'Pri', u'私人'),        
    )

def index(request, work_catalog):
    user = request.user
    works = Work.objects.all()
    if 'fiction' in work_catalog:
        works = works.filter(catalog__name='文字').filter(privacy='Pub')
        name = "文字"
    if 'illust' in work_catalog:
        works = works.filter(catalog__name='图集').filter(privacy='Pub')
        name = "图集"
    if 'comic' in work_catalog:
        works = works.filter(catalog__name='漫画').filter(privacy='Pub')
        name = "漫画"
        
    context = {}
    context['user'] = user
    context['works'] = works
    rand = []
    if works.count() > 8:
        num = 8
        for i in range(num):
            nw = random.choice(works)
            while nw in rand:
                nw = random.choice(works)
            rand.append(nw)
    else:
        rand = works
    
    all_sub_class = SubTabClass.objects.filter(parent_tab__tab_model_name='work')
    context['rand'] = rand
    context['new'] = works.order_by('-date')[:3]
    context['new2'] = works.order_by('-date')[4:7]
    context['work_catalog'] = work_catalog
    context['name'] = name
    ranks = Board.objects.all().order_by('-id')[0].get_board(work_catalog)
    context['ranks'] = ranks
    recommand = Recommand.objects.all().order_by('-id')[0].get_recommand(work_catalog)
    context['recommand'] = recommand
    context['tags'] = all_sub_class
    context['feature'] = Recommand.objects.all().order_by('-id')[0].get_feature(work_catalog)
    return render_to_response('work/index.shtml', context)
    
def home(request, work_id):
    user = request.user
    try:
        work = Work.objects.get(pk=work_id)
    except:
        raise Http404
    #print work.name
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    context = {}
    context['user'] = user
    context['work'] = work
    context['object'] = work
    comment = work.comment.all().order_by('-id')
    
    paginator = Paginator(comment, 10) # Show 25 contacts per page
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        n = paginator.page(page)
    except (EmptyPage, InvalidPage):
        n = paginator.page(paginator.num_pages)
    
    context['comments'] = n
    if im_boss or im_in or im_friend or im_viewer:
        return render_to_response('work/home.shtml', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})

@login_required  
def add_work(request):
    user = request.user
    try:
        work_catalog = request.GET.get('work_catalog')        
        if 'fiction' in work_catalog:
            catalogs = Catalog.objects.filter(name='文字')
        elif 'illust' in work_catalog:
            catalogs = Catalog.objects.filter(name__contains='图集').exclude(name__contains='实体')
        elif 'comic' in work_catalog:
            catalogs = Catalog.objects.filter(name__contains='漫画').exclude(name__contains='实体')
    except:
        work_catalog = None
        #catalogs = Catalog.objects.exclude(name__contains='实体')
        catalogs = Catalog.objects.filter(name__in=['文字', '图集', '漫画'])
    context = {}
    context['user'] = user
    context['catalogs'] = catalogs
    context['privacy'] = Work.PRIVACY_CHOICES
    new_work = Work(founder=user, name='请在这里填写作品名称', privacy='Pub', intro='请在这里填写作品简介', catalog=Catalog.objects.get(name='文字'), cover='cover/default_cover.gif')
    context['work'] = new_work
    if request.method == 'POST':
        uploaded = request.FILES.get('upload_cover')
        new_work.name = request.POST.get('name')
        new_work.privacy = request.POST.get('privacy')
        new_work.intro = request.POST.get('intro')
        catalog_id = request.POST.get('catalog_id')
        new_work.catalog = Catalog.objects.get(pk=int(catalog_id))
        new_work.save()
        if uploaded:
            new_work.cover.save('work_%s_cover.jpg' % new_work.id, ContentFile(uploaded.read()), save=True)
        object_type = ContentType.objects.get(name='work')
        object_id = new_work.id
        notification.send([user], "new_work", {"from_user": user, "work":new_work}, sender=user, object_type=object_type, object_id=object_id)
        return HttpResponseRedirect('/work/%s/edit/tab/' % new_work.id)
    return render_to_response('work/add_work.shtml', context)
    
@login_required  
def edit_work(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    context = {}
    context['user'] = user
    catalogs = Catalog.objects.filter(name__in=['文字', '图集', '漫画'])
    context['catalogs'] = catalogs
    context['work'] = work
    context['privacy'] = Work.PRIVACY_CHOICES
    im_boss = user == work.founder
    if im_boss:
        if request.method == 'POST':
            uploaded = request.FILES.get('upload_cover')
            if uploaded:
                if 'default_cover.gif' not in work.cover.name:
                    work.cover.delete(save=True)
                work.cover.save('work_%s_cover.jpg' % work.id, ContentFile(uploaded.read()), save=True)
            work.name = request.POST.get('name')
            work.privacy = request.POST.get('privacy')
            work.intro = request.POST.get('intro')
            catalog_id = request.POST.get('catalog_id')
            work.catalog = Catalog.objects.get(pk=int(catalog_id))
            work.save()
            return HttpResponseRedirect(work.get_absolute_url())
        return render_to_response('work/edit_work.shtml', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
@login_required  
def delete_work(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    im_boss = user == work.founder
    if im_boss:
        contenttype = ContentType.objects.get(name='work')
        notes = notification.Notice.objects.filter(object_type=contenttype, object_id=work.id)
        for n in notes:
            n.delete()
        if 'default_cover.gif' not in work.cover.name:
            work.cover.delete(save=True)
        work.delete()
        return HttpResponseRedirect('/%s/' % user.username)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
@login_required  
def edit_tab(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    options = work.catalog.option.all()
    f_tab = TabClass.objects.filter(tab_model_name='work')
    tabs = SubTabClass.objects.filter(parent_tab__tab_model_name='work')
    work_tab = work.tab.all()
    context = {}
    context['user'] = user
    catalogs = Catalog.objects.filter(name__in=[u'文字', u'图集', u'漫画'])
    context['catalogs'] = catalogs
    context['work'] = work
    context['options'] = options
    context['tabs'] =tabs
    context['f_tab'] =f_tab
    context['work_tab'] = work_tab
    
    im_boss = user == work.founder
    if im_boss:
        if request.method == 'POST':
            for op in options:
                try:
                    v = Value.objects.get(work=work, option=op)
                except:
                    v = Value(work=work, option=op)
                v.value = request.POST.get(op.name)
                v.save()
            work.tab.clear()
            for f in f_tab:
                sub_name = request.POST.get('select_%s' % f.id)
                if not sub_name:
                    continue
                new_tab = SubTabClass.objects.get(sub_name=sub_name)
                work.tab.add(new_tab)
            work.save()
            return HttpResponseRedirect(work.get_absolute_url())
        else:
            values = []
            for op in options:
                try:
                    v = Value.objects.get(work=work, option=op)
                    values.append(v)
                except:
                    v = None                  
            context['values'] = values
        return render_to_response('work/edit_tab.shtml', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})

def show_text(request, work_id):
    text_chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    try:
        section_id = int(request.GET.get('section_id'))
    except:
        try:
            section_id = text_chapter.section.all()[0].id
        except:
            return HttpResponseRedirect('/work/%s/' % work_id)
    the_section = TextSection.objects.get(id=section_id)
    nexts = []
    the_sec = the_section
    for i in range(3):
        try:
            next = the_sec.get_next_by_date(chapter=text_chapter)
            the_sec = next
            if next:
                nexts.append(next)
        except:
            next = None
            break;
    try:
        pre = the_section.get_previous_by_date(chapter=text_chapter)
    except:
        pre = None


    work = Work.objects.get(pk=work_id)
    user = request.user
    im_boss = user == work.founder or user == text_chapter.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    context = {}

    comment = ChapterComment.objects.filter(work=work, text=text_chapter).order_by('-id')
    paginator = Paginator(comment, 10) # Show 25 contacts per page
    page = 1
    n = paginator.page(page)

    context['comments'] = n
    
    if im_boss or im_in or im_friend or im_viewer:
        context['user'] = user
        context['work'] = work
        context['text_chapter'] = text_chapter
        context['section'] = the_section
        context['pre'] = pre
        context['nexts'] = nexts
        context['object'] = text_chapter
        return render_to_response('work/show_text_chapter.shtml', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
def refresh_text_section(request, work_id):
    text_chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    try:
        section_id = int(request.GET.get('section_id'))
    except:
        try:
            section_id = text_chapter.section.all()[0].id
        except:
            return HttpResponseRedirect('/work/%s/' % work_id)
    the_section = TextSection.objects.get(id=section_id)
    nexts = []
    the_sec = the_section
    for i in range(3):
        try:
            next = the_sec.get_next_by_date(chapter=text_chapter)
            the_sec = next
            if next:
                nexts.append(next)
        except:
            next = None
            break;
    try:
        pre = the_section.get_previous_by_date(chapter=text_chapter)
    except:
        pre = None


    work = Work.objects.get(pk=work_id)
    user = request.user
    im_boss = user == work.founder or user == text_chapter.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    context = {}

    comment = ChapterComment.objects.filter(work=work, text=text_chapter).order_by('-id')
    paginator = Paginator(comment, 10) # Show 25 contacts per page
    page = 1
    n = paginator.page(page)

    context['comments'] = n
    
    if im_boss or im_in or im_friend or im_viewer:
        context['user'] = user
        context['work'] = work
        context['text_chapter'] = text_chapter
        context['section'] = the_section
        context['pre'] = pre
        context['nexts'] = nexts
        context['object'] = text_chapter
        return render_to_response('work/text_section.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
def refresh_pre(request, work_id):
    text_chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    try:
        section_id = int(request.GET.get('section_id'))
    except:
        try:
            section_id = text_chapter.section.all()[0].id
        except:
            return HttpResponseRedirect('/work/%s/' % work_id)
    the_section = TextSection.objects.get(id=section_id)
    nexts = []
    the_sec = the_section
    for i in range(3):
        try:
            next = the_sec.get_next_by_date(chapter=text_chapter)
            the_sec = next
            if next:
                nexts.append(next)
        except:
            next = None
            break;
    try:
        pre = the_section.get_previous_by_date(chapter=text_chapter)
    except:
        pre = None


    work = Work.objects.get(pk=work_id)
    user = request.user
    im_boss = user == work.founder or user == text_chapter.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    context = {}

    comment = ChapterComment.objects.filter(work=work, text=text_chapter).order_by('-id')
    paginator = Paginator(comment, 10) # Show 25 contacts per page
    page = 1
    n = paginator.page(page)

    context['comments'] = n
    
    if im_boss or im_in or im_friend or im_viewer:
        context['user'] = user
        context['work'] = work
        context['text_chapter'] = text_chapter
        context['section'] = the_section
        context['pre'] = pre
        context['nexts'] = nexts
        context['object'] = text_chapter
        return render_to_response('work/pre.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
def refresh_section(request, work_id):
    text_chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    try:
        section_id = int(request.GET.get('section_id'))
    except:
        try:
            section_id = text_chapter.section.all()[0].id
        except:
            return HttpResponseRedirect('/work/%s/' % work_id)
    the_section = TextSection.objects.get(id=section_id)
    nexts = []
    the_sec = the_section
    for i in range(3):
        try:
            next = the_sec.get_next_by_date(chapter=text_chapter)
            the_sec = next
            if next:
                nexts.append(next)
        except:
            next = None
            break;
    try:
        pre = the_section.get_previous_by_date(chapter=text_chapter)
    except:
        pre = None


    work = Work.objects.get(pk=work_id)
    user = request.user
    im_boss = user == work.founder or user == text_chapter.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    context = {}

    comment = ChapterComment.objects.filter(work=work, text=text_chapter).order_by('-id')
    paginator = Paginator(comment, 10) # Show 25 contacts per page
    page = 1
    n = paginator.page(page)

    context['comments'] = n
    
    if im_boss or im_in or im_friend or im_viewer:
        context['user'] = user
        context['work'] = work
        context['text_chapter'] = text_chapter
        context['section'] = the_section
        context['pre'] = pre
        context['nexts'] = nexts
        context['object'] = text_chapter
        return render_to_response('work/section.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
def refresh_next(request, work_id):
    text_chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    try:
        section_id = int(request.GET.get('section_id'))
    except:
        try:
            section_id = text_chapter.section.all()[0].id
        except:
            return HttpResponseRedirect('/work/%s/' % work_id)
    the_section = TextSection.objects.get(id=section_id)
    nexts = []
    the_sec = the_section
    for i in range(3):
        try:
            next = the_sec.get_next_by_date(chapter=text_chapter)
            the_sec = next
            if next:
                nexts.append(next)
        except:
            next = None
            break;
    try:
        pre = the_section.get_previous_by_date(chapter=text_chapter)
    except:
        pre = None


    work = Work.objects.get(pk=work_id)
    user = request.user
    im_boss = user == work.founder or user == text_chapter.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    context = {}

    comment = ChapterComment.objects.filter(work=work, text=text_chapter).order_by('-id')
    paginator = Paginator(comment, 10) # Show 25 contacts per page
    page = 1
    n = paginator.page(page)

    context['comments'] = n
    
    if im_boss or im_in or im_friend or im_viewer:
        context['user'] = user
        context['work'] = work
        context['text_chapter'] = text_chapter
        context['section'] = the_section
        context['pre'] = pre
        context['nexts'] = nexts
        context['object'] = text_chapter
        return render_to_response('work/next.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
def show_gallery(request, work_id):
    gallery_chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
    work = Work.objects.get(pk=work_id)
    user = request.user
    im_boss = user == work.founder or user == gallery_chapter.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    context = {}
    
    comment = ChapterComment.objects.filter(work=work, gallery=gallery_chapter).order_by('-id')
    paginator = Paginator(comment, 10) # Show 25 contacts per page
    page = 1
    n = paginator.page(page)

    context['comments'] = n
    if im_boss or im_in or im_friend or im_viewer:
        context['user'] = user
        context['work'] = work
        context['chapter'] = gallery_chapter
        context['object'] = gallery_chapter
        return render_to_response('work/show_gallery_chapter.shtml', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})

@login_required  
def sync_text(request, work_id):
    text_chapter = TextChapter.objects.get(pk=int(request.GET.get('text_id')))
    work = Work.objects.get(pk=work_id)
    user = request.user
    im_boss = user == work.founder or user == text_chapter.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss:
        context = {}
        context['user'] = user
        context['work'] = work
        context['chapter'] = text_chapter
        other_work = []
        for w in Work.objects.all():
            if w.founder == user or user in w.get_members():
                other_work.append(w)
        #other_work = list(user.own_work.all()).extend(list(user.in_work.all()))
        #print other_work
        context['other_work'] = other_work
        if request.method == 'POST':
            try:
                other_work = Work.objects.get(pk=request.POST.get('other_work_id'))
            except:
                return HttpResponseRedirect(work.get_absolute_url())
            new_chapter = TextChapter(work=other_work, from_work=work, title=text_chapter.title, abstract=text_chapter.abstract, auther=text_chapter.auther)
            new_chapter.save()
            for s in text_chapter.section.all():
                new_section = TextSection(chapter=new_chapter, title=s.title, auther=s.auther, content=s.content)
                new_section.save()
            object_type = ContentType.objects.get(name='text chapter')
            notification.send([user], "sync_text", {"from_user": user, "other_work":other_work, "text":new_chapter}, sender=user, object_type=object_type, object_id=new_chapter.id)
            return HttpResponseRedirect(work.get_absolute_url())
        return render_to_response('work/sync_text_chapter.shtml', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})

@login_required
def sync_gallery(request, work_id):
    gallery_chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
    work = Work.objects.get(pk=work_id)
    user = request.user
    im_boss = user == work.founder or user == gallery_chapter.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss:
        context = {}
        context['user'] = user
        context['work'] = work
        context['chapter'] = gallery_chapter
        other_work = []
        #TODO:这尼玛什么情况····
        for w in Work.objects.all():
            if w.founder == user or user in w.get_members():
                other_work.append(w)
        #other_work = list(user.own_work.all()).extend(list(user.in_work.all()))
        #print other_work
        context['other_work'] = other_work
        if request.method == 'POST':
            try:
                other_work = Work.objects.get(pk=request.POST.get('other_work_id'))
            except:
                return HttpResponseRedirect(work.get_absolute_url())
            new_chapter = GalleryChapter(work=other_work, from_work=work, title=gallery_chapter.title, abstract=gallery_chapter.abstract, auther=gallery_chapter.auther)
            new_chapter.save()
            for s in gallery_chapter.section.all():
                #TODO:需要复制一份图像，以免一边删除，另一边也被删除
                new_section = GallerySection(chapter=new_chapter, title=s.title, auther=s.auther, picture=s.picture, content=s.content)
                new_section.save()
            object_type = ContentType.objects.get(name='gallery chapter')
            notification.send([user], "sync_gallery", {"from_user": user, "other_work":other_work, "gallery":new_chapter}, sender=user, object_type=object_type, object_id=new_chapter.id)
            return HttpResponseRedirect(work.get_absolute_url())
        return render_to_response('work/sync_gallery_chapter.shtml', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
@login_required
def show_text_section(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    try:
        section_id = request.GET.get('section_id')
    except:
        section_json = {}
        section_json['title'] = ""
        section_json['content'] = ""
        return HttpResponse(simplejson.dumps(section_json), mimetype='application/json')
    section = TextSection.objects.get(pk=int(section_id))
    section_json = {}
    section_json['title'] = section.title
    section_json['content'] = section.content
    return HttpResponse(simplejson.dumps(section_json), mimetype='application/json')

#@csrf_exempt 
@login_required
def edit_text_section(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    context = {}
    try:
        chapter = TextChapter.objects.get(pk=int(request.GET.get('text_id')))
    except:
        return HttpResponseRedirect(work.get_absolute_url())
    context['user'] = user
    context['work'] = work
    context['chapter'] = chapter
    if chapter.work != work:
        return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    have_right = user == chapter.auther or user == work.founder
    if have_right:
        if request.method == 'POST':
            try:
                req = simplejson.loads(request.raw_post_data)
                title = req['title']
                content = req['content']
                if not title or not content:
                    raise NoData
                try:
                    section_id = request.GET.get('section_id')
                    new_section = TextSection.objects.get(pk=int(section_id))
                    new_section.title = title
                    new_section.content = content
                except:
                    new_section = TextSection(title=title, content=content, auther=chapter.auther, chapter=chapter)
                new_section.save()
                new_history = UpdateHistory(user=user, work=work, mode='modify', text=chapter)
                new_history.save()
                return HttpResponse('...')
            except NoData:
                return HttpResponseRedirect(work.get_absolute_url())
        return render_to_response('work/edit_text.shtml', context)
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
def refresh_text(request, work_id):
    chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    return render_to_response('inc/form/upload-contents-chapter.html', {"chapter":chapter})
    
@login_required
def delete_text_section(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    
    if user == work.founder or user == chapter.auther:
        section = TextSection.objects.get(pk=int(request.GET.get('section_id')))
        chapter_id = section.chapter.id
        section.delete()
        return HttpResponseRedirect('/work/%s/text/section/?text_id=%s' % (work.id, chapter_id))
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
@login_required
def show_gallery_section(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    section_id = request.GET.get('section_id')
    section = GallerySection.objects.get(pk=int(section_id))
    section_json = {}
    section_json['title'] = section.title
    section_json['section_id'] = section.id
    section_json['content'] = section.content
    return HttpResponse(simplejson.dumps(section_json), mimetype='application/json')
    
#@csrf_exempt 
@login_required
def edit_gallery_section(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    context = {}
    try:
        chapter = GalleryChapter.objects.get(pk=int(request.GET.get('gallery_id')))
    except:
        return HttpResponseRedirect(work.get_absolute_url())
    context['user'] = user
    context['work'] = work
    context['chapter'] = chapter
    if chapter.work != work:
        return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    have_right = user == chapter.auther or user == work.founder
    if have_right:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            if not title:
                return HttpResponseRedirect(work.get_absolute_url())
            try:
                section_id = request.POST.get('section_id')
                #print "section id is %s" % section_id  
                new_section = GallerySection.objects.get(pk=int(section_id))
                new_section.title = title
                new_section.content = content
                #new_section.save()
            except:
                new_section = GallerySection(title=title, auther=chapter.auther, chapter=chapter, content=content, picture='cover/default_cover.gif')
                #new_section.save()
            new_history = UpdateHistory(user=user, work=work, mode='modify', gallery=chapter)
            #new_history.save()
            picture = request.FILES.get('picture')
              
            try:
                if 'image' not in picture.content_type:
                    raise 'content type wrong'
                if 'default_cover.gif' not in new_section.picture.name:
                    new_section.picture.delete(save=True)
                new_section.save()
                new_section.picture.save('work_%s_%s.jpg' % (work.id, new_section.id), ContentFile(picture.read()), save=True)
            except:
                new_section.save()
            new_history.save()
            return render_to_response('work/edit_gallery.shtml', context)
        return render_to_response('work/edit_gallery.shtml', context)
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
def refresh_gallery(request, work_id):
    chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    return render_to_response('inc/form/upload-contents-chapter.html', {"chapter":chapter})

@login_required
def delete_gallery_section(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    
    if user == work.founder or user == chapter.auther:
        section = GallerySection.objects.get(pk=int(request.GET.get('section_id')))
        chapter_id = section.chapter.id
        if 'default_cover.gif' not in section.picture.name:
            section.picture.delete(save=True)
        section.delete()
        return HttpResponseRedirect('/work/%s/gallery/section/?gallery_id=%s' % (work.id, chapter_id))
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
        
@login_required
def edit_text(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'

    if request.GET.get('action') == 'edit' :
        chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
        im_boss = user == work.founder or user == chapter.auther
        if im_boss:
            context = {}
            context['user'] = user
            context['work'] = work
            context['chapter'] = chapter
            context['new'] = False
            if request.method == 'POST':
                title = request.POST.get('title')
                abstract = request.POST.get('abstract')
                chapter.title = title
                chapter.abstract = abstract
                chapter.save()
                object_type = ContentType.objects.get(name='text chapter')
                object_id = chapter.id
                notification.send([user], "edit_text", {"from_user": user, "text":chapter, "work":work}, object_type=object_type, object_id=object_id)
                new_history = UpdateHistory(user=user, work=work, mode='modify', text=chapter)
                new_history.save()
                return HttpResponseRedirect(work.get_absolute_url())
            return render_to_response('work/edit_text_meta.shtml', context)
    if request.GET.get('action') == 'new' and im_boss or im_in:
        if request.GET.get('step') == '1':
            context = {}
            context['user'] = user
            context['work'] = work
            context['new'] = True
            chapter = TextChapter(title='在这里输入标题', abstract='在这里输入摘要', auther=user, work=work)
            context['chapter'] = chapter
            if request.method == 'POST':
                title = request.POST.get('title')
                abstract = request.POST.get('abstract')
                chapter.title = title
                chapter.abstract = abstract
                chapter.save()
                object_type = ContentType.objects.get(name='text chapter')
                object_id = chapter.id
                notification.send([user], "new_text", {"from_user": user, "text":chapter, "work":work}, sender=user, object_type=object_type, object_id=object_id)
                new_history = UpdateHistory(user=user, work=work, mode='add', text=chapter)
                new_history.save()
                return HttpResponseRedirect('/work/%s/edit/text/?action=new&step=2&chapter_id=%s' % (work.id, chapter.id))
            return render_to_response('work/new_text.shtml', context)
        if request.GET.get('step') == '2':
            context = {}
            context['user'] = user
            context['work'] = work
            context['new'] = True
            chapter = TextChapter.objects.get(pk=int(request.GET.get('chapter_id')))
            context['chapter'] = chapter
            if request.method == 'POST':
                title = request.POST.get('title')
                abstract = request.POST.get('abstract')
                chapter.title = title
                chapter.abstract = abstract
                chapter.save()
                object_type = ContentType.objects.get(name='text chapter')
                object_id = chapter.id
                notification.send([user], "edit_text", {"from_user": user, "text":chapter, "work":work}, sender=user, object_type=object_type, object_id=object_id)
                new_history = UpdateHistory(user=user, work=work, mode='add', text=chapter)
                new_history.save()
                return HttpResponseRedirect(work.get_absolute_url())
            return render_to_response('work/edit_text.shtml', context)
    if request.GET.get('action') == 'del':
        chapter = TextChapter.objects.get(pk=int(request.GET.get('text_id')))
        im_boss = user == work.founder or user == chapter.auther
        if im_boss:
            context = {}
            context['user'] = user
            context['work'] = work
            context['chapter'] = chapter
            new_history = UpdateHistory(user=user, work=work, mode='remove', chapter_name=chapter.title)
            new_history.save()
            object_type = ContentType.objects.get(name='text chapter')
            object_id = chapter.id
            notes = notification.Notice.objects.filter(object_type=object_type, object_id=object_id)
            for n in notes:
                n.delete()
            chapter.delete()
            return HttpResponseRedirect(work.get_absolute_url())
        return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    return HttpResponseRedirect(work.get_absolute_url())
    
#@csrf_exempt 
@login_required
def edit_gallery(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    
    if request.GET.get('action') == 'edit' :
        chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
        im_boss = user == work.founder or user == chapter.auther
        if im_boss:
            context = {}
            context['user'] = user
            context['work'] = work
            context['chapter'] = chapter
            context['new'] = False
            if request.method == 'POST':
                title = request.POST.get('title')
                abstract = request.POST.get('abstract')
                chapter.title = title
                chapter.abstract = abstract
                chapter.save()
                object_type = ContentType.objects.get(name='gallery chapter')
                object_id = chapter.id
                notification.send([user], "edit_gallery", {"from_user": user, "gallery":chapter, "work":work}, sender=user, object_type=object_type, object_id=object_id)
                new_history = UpdateHistory(user=user, work=work, mode='modify', gallery=chapter)
                new_history.save()
                return HttpResponseRedirect(work.get_absolute_url())
            return render_to_response('work/edit_gallery_meta.shtml', context)
    if request.GET.get('action') == 'new' and im_boss or im_in:
        context = {}
        context['user'] = user
        context['work'] = work
        context['new'] = True
        chapter = GalleryChapter(title='在这里输入标题', abstract='在这里输入摘要', work=work, auther=user)
        context['chapter'] = chapter
        if request.method == 'POST':
            title = request.POST.get('title')
            abstract = request.POST.get('abstract')
            chapter.title = title
            chapter.abstract = abstract
            chapter.save()
            object_type = ContentType.objects.get(name='gallery chapter')
            object_id = chapter.id
            notification.send([user], "new_gallery", {"from_user": user, "gallery":chapter, "work":work}, sender=user, object_type=object_type, object_id=object_id)
            new_history = UpdateHistory(user=user, work=work, mode='add', gallery=chapter)
            new_history.save()
            return HttpResponseRedirect('/work/%s/gallery/section/?gallery_id=%s' % (work.id, chapter.id))
            return HttpResponseRedirect('/work/%s/edit/gallery/?action=edit&gallery_id=%s' % (work.id, chapter.id))
        return render_to_response('work/new_gallery.shtml', context)
    if request.GET.get('action') == 'del':
        chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
        im_boss = user == work.founder or user == chapter.auther
        if im_boss:
            context = {}
            context['user'] = user
            context['work'] = work
            context['chapter'] = chapter
            new_history = UpdateHistory(user=user, work=work, mode='remove', chapter_name=chapter.title)
            new_history.save()
            object_type = ContentType.objects.get(name='gallery chapter')
            object_id = chapter.id
            notes = notification.Notice.objects.filter(object_type=object_type, object_id=object_id)
            for n in notes:
                n.delete()
            for s in chapter.section.all():
                if 'default_cover.gif' not in s.picture.name:
                    s.picture.delete(save=True)
            chapter.delete()
            return HttpResponseRedirect(work.get_absolute_url())
            #return render_to_response('work/edit_gallery.html', context)
    return HttpResponseRedirect(work.get_absolute_url())

@login_required
def edit_links(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss:
        clubs = user.own_club.all().expend(user.charge_club.all()).expend(user.club_in.all())
        club = work.club
        context = {}
        context['user'] = user
        context['work'] = work
        context['club'] = club
        context['clubs'] = clubs
        if request.method == 'POST':
            club_id = request.POST.get('club_id')
            if club_id != '0':
                new_club = Club.objects.get(pk=club_id)
            else:
                new_club = None
            work.club = new_club
            work.save()
            return HttpResponseRedirect('.')
        return render_to_response('work/edit_links.html', context)
    return Http404

@login_required
def apply_member(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in:
        return render_to_response('error.html', {'error':'您已经在这里了'})
    context = {}
    context['user'] = user
    context['work'] = work
    the_user_abilities = user.get_profile().ability.all()
    f_ability = []
    for tua in the_user_abilities:
        f_ability.append(tua.parent_tab)
    f_ability = list(set(f_ability))
    context['f_ability'] = f_ability
    if request.method == 'POST':
        ability = SubTabClass.objects.get(pk=int(request.POST.get('ability_id')))
        reason = request.POST.get('reason')
        exsist = Membership.objects.filter(user=user, work=work)
        if exsist:
            HttpResponse("你已经对此项目进行了申请")
        new_member = Membership(user=user, work=work, from_user=user, reason=reason, ability=ability, status='App')
        new_member.save()
        object_type = ContentType.objects.get(name='work')
        object_id = work.id
        notification.send([work.founder], "work_apply", {"from_user": user, "work":work, "membership":new_member}, sender=user, object_type=object_type, object_id=object_id)
        work.founder.get_profile().unread_notes += 1
        work.founder.get_profile().save()
        return HttpResponseRedirect(work.get_absolute_url())
    return render_to_response('work/apply_member.shtml', context)
    
@login_required
def invite_member(request, username):
    user = request.user
    
    to_user = User.objects.get(username=username)
    #TODO:需要注意work是好友可见，被邀请的人不是好友的情况
    context = {}
    context['user'] = user
    context['to_user'] = to_user
    context['works'] = user.own_work.all
    if request.method == 'POST':
        work = Work.objects.get(pk=int(request.POST.get('work_id')))
        im_boss = to_user == work.founder
        im_in = work.privacy == 'Pri' and to_user in work.get_members()
        if im_boss or im_in:
            return render_to_response('error.html', {'error':'TA已经在这里了'})
        if not user == work.founder:
            return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
        ability = SubTabClass.objects.get(pk=int(request.POST.get('ability_id')))
        reason = request.POST.get('reason')
        exsist = Membership.objects.filter(user=to_user, work=work)
        if exsist:
            HttpResponse("你已经对此用户进行了邀请")
        new_member = Membership(user=to_user, work=work, from_user=user, reason=reason, status='Inv')
        new_member.save()
        object_type = ContentType.objects.get(name='work')
        object_id = work.id
        notification.send([to_user], "work_invite", {"from_user": user, "work":work, "membership":new_member}, sender=user, object_type=object_type, object_id=object_id)
        to_user.get_profile().unread_notes += 1
        to_user.get_profile().save()
        return HttpResponseRedirect('/%s/' % to_user.username)
    the_user_abilities = to_user.get_profile().ability.all()
    f_ability = []
    for tua in the_user_abilities:
        f_ability.append(tua.parent_tab)
    f_ability = list(set(f_ability))
    context['f_ability'] = f_ability
    return render_to_response('work/invite_member.shtml', context)
    
@login_required
def accept_member(request):
    user = request.user
    membership = Membership.objects.get(pk=request.GET.get('membership_id'))
    im_boss = user == membership.user or user == membership.work.founder
    if im_boss:
        if membership.status == 'Agr':
            return render_to_response('error.html', {'error':"你已经同意了这个申请/邀请"})
        membership.status = 'Agr'
        membership.save()
        work = membership.work
        from_user = User.objects.get(username=membership.from_user)
        from_user.get_profile().unread_notes += 1
        from_user.get_profile().save()
        object_type = ContentType.objects.get(name='work')
        object_id = work.id
        notification.send([from_user], "work_accept", {"from_user": user, "work":work}, sender=user, object_type=object_type, object_id=object_id)
        return HttpResponseRedirect(work.get_absolute_url())
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    

@login_required
def deny_member(request):
    user = request.user
    try:
        membership = Membership.objects.get(pk=int(request.GET.get('membership_id')))
    except:
       return render_to_response('error.html', {'error':"该申请/邀请不存在，或已经拒绝"})
    im_boss = user == membership.work.founder
    im_boss = user == membership.user or user == membership.work.founder
    if im_boss:
        if membership.status == 'Agr':
            return render_to_response('error.html', {'error':"你已经同意了这个申请/邀请"})
        membership.delete()
        #notification.send([membership.from_user], "work_deny", {"from_user": user, "work":work})
        return HttpResponseRedirect(membership.work.get_absolute_url())
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
def show_issue(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    issues = work.issue.all()
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in or im_friend or im_viewer:
        context = {}
        context['user'] = user
        context['work'] = work
        context['issues'] = issues
        return render_to_response('work/show_issue.shtml', context)
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
def view_issue(request, work_id, issue_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    issue = Issue.objects.get(pk=issue_id)
    im_boss = user == work.founder or user == issue.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in or im_friend or im_viewer:
        context = {}
        context['user'] = user
        context['work'] = work
        context['issue'] = issue
        return render_to_response('work/view_issue.shtml', context)
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})

@login_required
def add_issue(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    issues = work.issue.all()
    im_boss = user == work.founder or user == issue.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            new_issue = Issue(title=title, content=content, work=work, auther=user)
            new_issue.save()
            return HttpResponseRedirect(work.get_absolute_url()+'issues/')
        context = {}
        context['user'] = user
        context['work'] = work
        return render_to_response('work/add_issue.shtml', context)
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
@login_required
def make_issue_done(request, work_id, issue_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    issue = Issue.objects.get(pk=issue_id)
    im_boss = user == work.founder or user == issue.auther
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in:
        issue.status = 0
        issue.save()
        return HttpResponseRedirect(work.get_absolute_url()+'issues/')
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
def show_history(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in or im_friend or im_viewer:
        context = {}
        context['user'] = user
        context['work'] = work
        history = work.history.all()
        paginator = Paginator(history, 20) # Show 25 contacts per page
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        # If page request (9999) is out of range, deliver last page of results.
        try:
            n = paginator.page(page)
        except (EmptyPage, InvalidPage):
            n = paginator.page(paginator.num_pages)
        
        context['history'] = n
        return render_to_response('work/show_history.shtml', context)
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
def refresh_history(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in or im_friend or im_viewer:
        context = {}
        context['user'] = user
        context['work'] = work
        history = work.history.all()
        paginator = Paginator(history, 20) # Show 25 contacts per page
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        # If page request (9999) is out of range, deliver last page of results.
        try:
            n = paginator.page(page)
        except (EmptyPage, InvalidPage):
            n = paginator.page(paginator.num_pages)
        
        context['history'] = n
        return render_to_response('inc/project/history.html', context)
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
def show_member(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    membership = Membership.objects.filter(work=work, status='Agr')
    member = []
    for m in membership:
        member.append(m.user)
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in or im_friend or im_viewer:
        context = {}
        context['user'] = user
        context['work'] = work
        context['member'] = member
        return render_to_response('work/show_member.shtml', context)
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})
    
def show_comment(request, work_id, text_id=None, gallery_id=None):
    work = Work.objects.get(pk=work_id)
    try:
        chapter_id = text_id
        chapter = TextChapter.objects.get(pk=int(chapter_id))
        comments = ChapterComment.objects.filter(work=work, text=chapter).order_by('-id')
    except:
        try:
            chapter_id = gallery_id
            chapter = GalleryChapter.objects.get(pk=int(chapter_id))
            comments = ChapterComment.objects.filter(work=work, gallery=chapter).order_by('-id')
        except:
            comments = ChapterComment.objects.filter(work=work).order_by('-id')
    return comments

def refresh_comment(request, work_id):
    work = Work.objects.get(pk=work_id)
    text_id = request.GET.get('text_id')
    gallery_id = request.GET.get('gallery_id')
    comment = show_comment(request, work_id, text_id, gallery_id)
    paginator = Paginator(comment, 10) # Show 25 contacts per page
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        n = paginator.page(page)
    except (EmptyPage, InvalidPage):
        n = paginator.page(paginator.num_pages)
    
    context = {}
    context['comments'] = n
    try:
        chapter = TextChapter.objects.get(pk=int(text_id))
    except:
        try:
            chapter = GalleryChapter.objects.get(pk=int(gallery_id))
        except:
            chapter = work
    context['object'] = chapter

    return render_to_response('inc/comments.html', context)

#@csrf_exempt
@login_required
def add_comment(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    im_boss = user == work.founder
    im_in = user in work.get_members()
    im_friend = work.privacy == 'Fri' and user in work.founder.relationships.friends()
    im_viewer = work.privacy == 'Pub'
    if im_boss or im_in or im_friend or im_viewer:
        text = gallery = None
        try:
            chapter_id = request.GET.get('text_id')
            text = TextChapter.objects.get(pk=int(chapter_id))
        except:
            try:
                chapter_id = request.GET.get('gallery_id')
                gallery = GalleryChapter.objects.get(pk=int(chapter_id))
            except:
                text = gallery = None

        try:
            req = simplejson.loads(request.raw_post_data)
            content = req['status']
            return_url = 1
        except:
            content = request.POST.get('status')
            return_url = 0
        #TODO:如果一开始就自动加入，就好了恩
        object = work
        the_user = work.founder
        if text != None or gallery != None:
            try:
                chapter_prefix = '<a href=%s>#%s#</a> ' % (text.get_absolute_url(), text.title)
                content = chapter_prefix+content
                object = text
                the_user = text.auther
            except:
                chapter_prefix = '<a href="%s">#%s#</a> ' % (gallery.get_absolute_url(), gallery.title)
                content = chapter_prefix+content
                object = gallery
                the_user = gallery.auther  
        object_type = ContentType.objects.get(name='work')
        object_id = work.id
        new_comment = ChapterComment(work=work, user=user, text=text, gallery=gallery, content=content)
        new_comment.save()
        if user != the_user:
            if the_user == work.founder:
                re_list = [work.founder]
            else:
                re_list = [work.founder, the_user]
            notification.send(re_list, "new_reply", {"from_user": user, "object":object, "work":work}, sender=user, object_type=object_type, object_id=object_id)
            for u in re_list:
                u.get_profile().unread_notes += 1
                u.get_profile().save()
        if not return_url:
            return HttpResponseRedirect('.')
        else:
            return HttpResponse('...')
    return render_to_response('error.html', {'error':'您没有权限访问这个页面'})

@login_required  
def del_comment(request):
    comment = request.GET.get('cid')
    user = request.user
    if user == comment.work.founder or comment.text in user.text_chapter.all() or comment.gallery in user.gallery_chapter.all():
        object_type = ContentType.objects.get(name='chapter comment')
        note = notification.Notice.objects.filter(object_type=object_type, object_id=comment.id)
        for n in note:
            if n.unseen and n.sender != request.user:
                n.recipient.get_profile().unread_notes -= 1
        note.delete()
        comment.delete()
        return HttpResponse('...')
    return HttpResponse('...')
    
@login_required 
def share_work(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    to_user = work.founder
    #if not to_user in user.relationships.following():
    #    status = get_object_or_404(RelationshipStatus, from_slug='following')
    #    request.user.relationships.add(to_user, status)
    #    '''
    #    notification.send([to_user], "following", {"from_user":request.user}, sender=user)
    #    to_user.get_profile().unread_notes += 1
    #    to_user.get_profile().save()
    #    '''
    try:
        ShareWork.objects.get(user_profile=user.get_profile(), work=work)
        return render_to_response("error.html", {'error':'您已经关注过这个作品了'})
    except:
        new_share = ShareWork(user_profile=user.get_profile(), work=work, reason='我就喜欢')
        new_share.save()
        work.collected += 1
        work.save()
        context = {}
        context['work'] = work
        context['user'] = user
        #return HttpResponseRedirect(work.get_absolute_url())
        return render_to_response("inc/project/info.shtml", context)
    
@login_required 
def refresh_info(request, work_id):
    user = request.user
    work = Work.objects.get(pk=work_id)
    context = {}
    context['work'] = work
    context['user'] = user
    if work in user.pushed.all():
        return render_to_response("inc/project/info.shtml", context)
    else:
        work.puship.add(user)
        work.push += 1
        work.push_today += 1
        work.save()
    return render_to_response("inc/project/info.shtml", context)