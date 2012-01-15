# -*- coding: UTF-8 -*-

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
from synclee.club.models import *
from synclee.notification import models as notification

def index(request):
    user = request.user
    
    clubs = Club.objects.all()
    context = {}
    context['user'] = user
    context['clubs'] = clubs
    return render_to_response('club/index.html', context)
    
def home(request, club_name):
    user = request.user
    context = {}
    club = Club.objects.get(name=club_name)
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.members.all()
    if True:
        context['user'] = user
        context['club'] = club
        return render_to_response('club/home.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
@login_required  
def add_club(request):
    user = request.user
    context = {}
    context['user'] = user
    #context['catalogs'] = catalogs
    new_club = Club(founder=user, name='请在这里填写社团名称', intro='请在这里填写社团简介')
    context['club'] = new_club
    if request.method == 'POST':
        new_club.name = request.POST.get('name')
        new_club.intro = request.POST.get('intro')
        new_club.save()
        #notification.send([user], "new_club", {"from_user": user, "club":new_club})
        return HttpResponseRedirect('/club/%s/' % new_club.id)
    return render_to_response('club/add_club.html', context)

def show_text(request, club_name):
    context = {}
    text_chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    club = Club.objects.get(name=club_name)
    
    user = request.user
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if True:
        context['user'] = user
        context['club'] = club
        context['text_chapter'] = text_chapter
        return render_to_response('club/show_text_chapter.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
def show_gallery(request, club_name):
    context = {}
    gallery_chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
    club = Club.objects.get(name=club_name)
    user = request.user
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if True:
        context['user'] = user
        context['club'] = club
        context['gallery_chapter'] = gallery_chapter
        return render_to_response('club/show_gallery_chapter.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})

@login_required
def edit_text_section(request, club_name):
    
    user = request.user
    club = Club.objects.get(name=club_name)
    chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if request.GET.get('action') == 'new' and im_boss:
        context = {}
        context['user'] = user
        context['club'] = club
        context['chapter'] = chapter
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            new_section = TextSection(title=title, content=content, auther=chapter.auther, chapter=chapter)
            new_section.save()
            return HttpResponseRedirect(chapter.get_absolute_url())
        return render_to_response('club/edit_text_section.html', context)
    if request.GET.get('action') == 'edit' and im_boss:
        section = TextSection.objects.get(pk=request.GET.get('section_id'))
        context = {}
        context['user'] = user
        context['club'] = club
        context['chapter'] = chapter
        context['section'] = section
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            new_section = TextSection(title=title, content=content, auther=chapter.auther, chapter=chapter)
            new_section.save()
            return HttpResponseRedirect(chapter.get_absolute_url())
        return render_to_response('club/edit_text_section.html', context)
    if request.GET.get('action') == 'del' and im_boss:
        section = TextSection.objects.get(pk=request.GET.get('section_id'))
        context = {}
        context['user'] = user
        context['club'] = club
        context['chapter'] = chapter
        context['section'] = section
        if request.method == 'POST':
            section.delete()
            return HttpResponseRedirect(chapter.get_absolute_url())
        return render_to_response('club/edit_text_section.html', context)
    return Http404

@login_required
def edit_gallery_section(request, club_name):
    
    user = request.user
    club = Club.objects.get(name=club_name)
    chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if request.GET.get('action') == 'new' and im_boss:
        context = {}
        context['user'] = user
        context['club'] = club
        context['chapter'] = chapter
        if request.method == 'POST':
            title = request.POST.get('title')
            picture = request.FILES.get('picture')
            new_section = GallerySection(title=title, picture=picture, auther=chapter.auther, chapter=chapter)
            new_section.save()
            return HttpResponseRedirect(chapter.get_absolute_url())
        return render_to_response('club/edit_gallery_section.html', context)
    if request.GET.get('action') == 'edit' and im_boss:
        section = GallerySection.objects.get(pk=request.GET.get('section_id'))
        context = {}
        context['user'] = user
        context['club'] = club
        context['chapter'] = chapter
        context['section'] = section
        if request.method == 'POST':
            title = request.POST.get('title')
            picture = request.FILES.get('picture')
            section.title = title
            filename = str(section.id)+'.jpg'
            section.picture.save(filename, picture, save=True)
            section.save()
            return HttpResponseRedirect(chapter.get_absolute_url())
        return render_to_response('club/edit_gallery_section.html', context)
    if request.GET.get('action') == 'del' and im_boss:
        section = GallerySection.objects.get(pk=request.GET.get('section_id'))
        context = {}
        context['user'] = user
        context['club'] = club
        context['chapter'] = chapter
        context['section'] = section
        if request.method == 'POST':
            section.delete()
            return HttpResponseRedirect(chapter.get_absolute_url())
        return render_to_response('club/edit_gallery_section.html', context)
    return Http404


def show_project_gallery(request, club_name, project_id):
    context = {}
    gallery_chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
    club = Club.objects.get(name=club_name)
    projcet = Project.objects.get(pk=project_id)
    user = request.user
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if True:
        context['user'] = user
        context['club'] = club
        context['gallery_chapter'] = gallery_chapter
        context['project'] = project
        return render_to_response('club/show_project_gallery_chapter.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})

@login_required
def edit_text(request, club_name):
    user = request.user
    club = Club.objects.get(name=club_name)
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    
    if request.GET.get('action') == 'edit' :
        chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
        im_boss = user == club.founder or user == chapter.auther
        if im_boss or im_charge:
            context = {}
            context['user'] = user
            context['club'] = club
            context['chapter'] = chapter
            context['new'] = False
            if request.method == 'POST':
                title = request.POST.get('title')
                abstract = request.POST.get('abstract')
                chapter.title = title
                chapter.abstract = abstract
                chapter.save()
                return HttpResponseRedirect(chapter.get_absolute_url())
            return render_to_response('club/edit_text.html', context)
    if request.GET.get('action') == 'new' and im_boss or im_in:
        context = {}
        context['user'] = user
        context['club'] = club
        context['new'] = True
        chapter = TextChapter(title='在这里输入标题', abstract='在这里输入摘要', club=club, auther=user)
        context['chapter'] = chapter
        if request.method == 'POST':
            title = request.POST.get('title')
            abstract = request.POST.get('abstract')
            chapter.title = title
            chapter.abstract = abstract
            chapter.save()
            notification.send([user], "new_club_text", {"from_user": user, "club":club, 'text':chapter})
            return HttpResponseRedirect(chapter.get_absolute_url())
        return render_to_response('club/edit_text.html', context)
    if request.GET.get('action') == 'del':
        chapter = TextChapter.objects.get(pk=request.GET.get('text_id'))
        im_boss = user == club.founder or user == chapter.auther
        if im_boss or im_charge:
            context = {}
            context['user'] = user
            context['club'] = club
            context['chapter'] = chapter
            if request.method == 'POST':
                chapter.delete()
                return HttpResponseRedirect(club.get_absolute_url())
            return render_to_response('club/edit_gallery.html', context)
    return Http404

@login_required
def edit_gallery(request, club_name):
    user = request.user
    club = Club.objects.get(name=club_name)
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    
    if request.GET.get('action') == 'edit' :
        chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
        im_boss = user == club.founder or user == chapter.auther
        if im_boss or im_charge:
            context = {}
            context['user'] = user
            context['club'] = club
            context['chapter'] = chapter
            context['new'] = False
            if request.method == 'POST':
                title = request.POST.get('title')
                abstract = request.POST.get('abstract')
                chapter.title = title
                chapter.abstract = abstract
                chapter.save()
                return HttpResponseRedirect(chapter.get_absolute_url())
            return render_to_response('club/edit_gallery.html', context)
    if request.GET.get('action') == 'new' and im_boss or im_charge:
        context = {}
        context['user'] = user
        context['club'] = club
        context['new'] = True
        chapter = GalleryChapter(title='在这里输入标题', abstract='在这里输入摘要', club=club, auther=user)
        context['chapter'] = chapter
        if request.method == 'POST':
            title = request.POST.get('title')
            abstract = request.POST.get('abstract')
            chapter.title = title
            chapter.abstract = abstract
            chapter.save()
            notification.send([user], "new_club_gallery", {"from_user": user, "club":club, 'gallery':chapter})
            return HttpResponseRedirect(chapter.get_absolute_url())
        return render_to_response('club/edit_gallery.html', context)
    if request.GET.get('action') == 'del':
        chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
        im_boss = user == club.founder or user == chapter.auther
        if im_boss or im_charge:
            context = {}
            context['user'] = user
            context['club'] = club
            context['chapter'] = chapter
            if request.method == 'POST':
                chapter.delete()
                return HttpResponseRedirect(club.get_absolute_url())
            return render_to_response('club/edit_gallery.html', context)
    return Http404

@login_required
def apply_member(request, club_name):
    user = request.user
    club = Club.objects.get(name=club_name)
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if im_boss or im_in or im_charge:
        return render_to_response('error.html', {'error':'您已经在这里了'})
    context = {}
    context['user'] = user
    context['club'] = club
    if request.method == 'POST':
        reason = request.POST.get('reason')
        new_member = ApplyClub(user=user, club=club, from_user=user, reason=reason, status='App')
        new_member.save()
        notification.send([club.founder], "club_apply", {"from_user": user, "club":club, "membership":new_member})
        return HttpResponseRedirect(club.get_absolute_url())
    return render_to_response('club/apply_member.html', context)
    
@login_required
def invite_member(request, club_name, username):
    user = request.user
    club = Club.objects.get(name=club_name)
    to_user = User.objects.get(username=username)
    im_boss = to_user == club.founder
    im_charge = to_user in club.manager.all()
    im_in = to_user in club.memebers.all()
    if im_boss or im_in or im_charge:
        return render_to_response('error.html', {'error':'TA已经在这里了'})
    if not user == club.founder or user in club.manager.all():
        return HttpResponse('U have no right to be here')
    #TODO:需要注意club是好友可见，被邀请的人不是好友的情况
    context = {}
    context['user'] = user
    context['to_user'] = to_user
    context['club'] = club
    if request.method == 'POST':
        ability = SubTabClass.objects.get(pk=request.POST.get('ability_id'))
        reason = request.POST.get('reason')
        new_member = ApplyClub(user=to_user, club=club, from_user=user, reason=reason, status='Inv')
        new_member.save()
        notification.send([to_user], "club_invite", {"from_user": user, "club":club, "membership":new_member})
        return HttpResponseRedirect(to_user.get_absolute_url())
    return render_to_response('club/invite_member.html', context)
    
@login_required
def accept_member(request, club_name):
    user = request.user
    club = Club.objects.get(name=club_name)
    membership = ApplyClub.objects.get(pk=request.GET.get('membership_id'))
    if im_boss or im_charge:
        membership.status = 'Agr'
        membership.save()
        club.member.add(membership.user)
        club.save()
        notification.send([membership.from_user], "club_accept", {"from_user": user, "club":club})
        return HttpResponseRedirect(club.get_absolute_url())
    return HttpResponse('U have no right to be here')
    

@login_required
def deny_member(request, club_name):
    user = request.user
    club = Club.objects.get(name=club_name)
    membership = ApplyClub.objects.get(pk=request.GET.get('membership_id'))
    if im_boss or im_charge:
        membership.delete()
        #notification.send([membership.from_user], "club_deny", {"from_user": user, "club":club})
        return HttpResponseRedirect(club.get_absolute_url())
    return HttpResponse('U have no right to be here')
    
def project_home(request, club_name, project_id):
    context = {}
    user = request.user
    club = Club.objects.get(name=club_name)
    roject = Project.objects.get(pk=project_id)
    im_boss = user == club.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if True:
        context['user'] = user
        context['club'] = club
        context['project'] = project
        return render_to_response('club/project_home.html', context)
    return render_to_response('error.html', {'error':'对不起，您没有权限访问当前页面'})
    
@login_required  
def add_project(request, club_name):
    user = request.user
    context = {}
    context['user'] = user
    context['catalogs'] = catalogs
    club = Club.objects.get(name=club_name)
    new_project = Project(founder=user, name='请在这里填写企划名称', intro='请在这里填写企划简介')
    new_project.save()
    new_chapter = GalleryChapter(founder=user, name='作品预览', intro='作品预览截图', project=new_project)
    new_chapter.save()
    context['project'] = new_project
    if request.method == 'POST':
        new_project.name = request.POST.get('name')
        new_project.intro = request.POST.get('intro')
        new_project.save()
        notification.send([user], "new_project", {"from_user": user, "club":club, "project":new_project})
    return render_to_response('club/add_project.html', context)
    
@login_required
def edit_project_work(request, club_name, project_id):
    user = request.user
    club = Club.objects.get(name=club_name)
    project = Project.objects.get(pk=project_id)
    im_boss = user == club.founder or user == project.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if im_boss or im_charge:
        #TODO:修正逻辑
        clubs = user.own_club.all().expend(user.charge_club.all()).expend(user.club_in.all())
        now_works = project.work.all()
        id_list = []
        for w in now_works:
            id_list.append(w.id)
        other_works = user.own_work.exclude(id__in=id_list)
        context = {}
        context['user'] = user
        context['club'] = club
        context['project'] = project
        context['now_works'] = now_works
        context['other_works'] = other_works
        if request.method == 'POST':
            work_id = request.POST.getlist('work_id')
            new_works = Work.objects.filter(id__in=work_id)
            for w in new_works:
                project.work.add(w)
                project.save()
            return HttpResponseRedirect('.')
        return render_to_response('club/edit_project_work.html', context)
    return Http404

@login_required
def edit_project_gallery(request, club_name, project_id):
    user = request.user
    club = Club.objects.get(name=club_name)
    project = Project.objects.get(pk=project_id)
    im_boss = user == club.founder or user == project.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    
    if request.GET.get('action') == 'edit' :
        chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
        if im_boss or im_charge:
            context = {}
            context['user'] = user
            context['club'] = club
            context['project'] = project
            context['chapter'] = chapter
            if request.method == 'POST':
                title = request.POST.get('title')
                picture = request.FILES.get('picture')
                section.title = title
                filename = str(section.id)+'.jpg'
                section.picture.save(filename, picture, save=True)
                section.save()
                return HttpResponseRedirect(chapter.get_absolute_url())
            return render_to_response('club/edit_project_gallery.html', context)
    return Http404

@login_required
def edit_project_gallery_section(request, club_name, project_id):
    user = request.user
    club = Club.objects.get(name=club_name)
    project = Project.objects.get(pk=project_id)
    chapter = GalleryChapter.objects.get(pk=request.GET.get('gallery_id'))
    im_boss = user == club.founder or user == project.founder
    im_charge = user in club.manager.all()
    im_in = user in club.memebers.all()
    if im_boss or im_charge:
        context = {}
        context['user'] = user
        context['club'] = club
        context['project'] = project
        context['chapter'] = chapter
        if request.GET.get('action') == 'new':
            if request.method == 'POST':
                title = request.POST.get('title')
                content = request.POST.get('content')
                new_section = GallerySection(title=title, content=content, auther=chapter.auther, chapter=chapter)
                new_section.save()
                return HttpResponseRedirect(chapter.get_absolute_url())
            return render_to_response('club/edit_project_gallery_section.html', context)
        if request.GET.get('action') == 'edit':
            section = GallerySection.objects.get(pk=request.GET.get('section_id'))
            context['section'] = section
            if request.method == 'POST':
                title = request.POST.get('title')
                picture = request.POST.get('content')
                section.title = title
                section.picture = picture
                section.save()
                return HttpResponseRedirect(chapter.get_absolute_url())
            return render_to_response('club/edit_project_gallery_section.html', context)
        if request.GET.get('action') == 'del':
            section = GallerySection.objects.get(pk=request.GET.get('section_id'))
            context['section'] = section
            if request.method == 'POST':
                section.delete()
                return HttpResponseRedirect(chapter.get_absolute_url())
            return render_to_response('club/edit_project_gallery_section.html', context)
    return Http404