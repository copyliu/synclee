# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response

from synclee.profiles.models import *
from synclee.tab.models import *
from synclee.relationships.models import RelationshipManager
from synclee.notification.models import Notice
from synclee.billboard.models import Board
from synclee.recommand.models import Recommand
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.contenttypes.models import ContentType
import random
from operator import attrgetter
from itertools import chain

def home(request):
    user = request.user
    context = {}
    ranks = Board.objects.all().order_by('-id')[0].get_board('all')
    recommand = Recommand.objects.all().order_by('-id')[0].get_recommand('all')
    works = Work.objects.all()
    context['ranks'] = ranks
    context['recommand'] = recommand
    context['feature'] = Recommand.objects.all().order_by('-id')[0].get_feature('all')
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
    context['rand'] = rand
    if user.is_authenticated():
        try:
            profile = user.get_profile()
        except:
            profile = None
        if not profile:
            return HttpResponseRedirect('/profiles/?first=true')
        
        context['user'] = user
        following_user = user.relationships.following()
        following_list = []
        for u in following_user:
            following_list.append(u)
        following_list.append(user)
        exclude_type = ['new_reply', 'new_message', 'work_apply', 'work_deny', 'work_accept', 'work_invite', 'club_apply', 'club_deny', 'club_accept', 'club_invite', 'following', 'edit_text', 'edit_gallery']
        exclude_extra_type = ['new_reply', 'new_message', 'work_apply', 'work_deny', 'work_accept', 'work_invite', 'club_apply', 'club_deny', 'club_accept', 'club_invite', 'following', 'edit_text', 'edit_gallery']
        notice_base = Notice.objects.exclude(notice_type__label__in=exclude_type)
        notice_base_extra = Notice.objects.exclude(notice_type__label__in=exclude_extra_type)
        notices = notice_base.filter(sender__in=following_list)
        object_type = ContentType.objects.get(name='work')
        object_text = ContentType.objects.get(name='text chapter')
        object_gallery = ContentType.objects.get(name='gallery chapter')
        share_work_list = user.get_profile().get_share_work_id()
        wlist = share_work_list['wlist']
        tlist = share_work_list['tlist']
        glist = share_work_list['glist']
        notice_share = notice_base_extra.exclude(sender__in=following_list)
        notices_work = notice_share.filter(object_type=object_type, object_id__in=wlist)
        notices_text = notice_share.filter(object_type=object_text, object_id__in=tlist)
        notices_gallery = notice_share.filter(object_type=object_gallery, object_id__in=glist)
        
        result_list = sorted(
        chain(notices, notices_work, notices_text, notices_gallery),
        key=attrgetter('added'), reverse=True)
        
        #result_list = result_list.reverse()
        paginator = Paginator(result_list, 10) # Show 25 contacts per page
        try:
            n = paginator.page(1)
        except (EmptyPage, InvalidPage):
            n = paginator.page(paginator.num_pages)
        context['notices'] = n
        return render_to_response('profiles/home.html', context)
    else:
        return render_to_response('index.shtml', context)
    
def people(request, username):
    people = User.objects.get(username=username)
    context = {}
    user = request.user
    context['user'] = user
    context['the_user'] = people
    in_work = []
    for m in Membership.objects.filter(user=people, status='Agr'):
        in_work.append(m.work)
    context['in_work'] = in_work
    exclude_type = ['new_reply', 'new_message', 'work_apply', 'work_deny', 'work_accept', 'work_invite', 'club_apply', 'club_deny', 'club_accept', 'club_invite', 'following', 'edit_text', 'edit_gallery']
    notices = Notice.objects.filter(sender=people).exclude(notice_type__label__in=exclude_type)
        
    paginator = Paginator(notices, 10) # Show 25 contacts per page

    try:
        n = paginator.page(1)
    except (EmptyPage, InvalidPage):
        n = paginator.page(paginator.num_pages)
    context['notices'] = n
    
    return render_to_response('profiles/people.html', context)

@login_required
def show_profile(request):
    user = request.user
    try:
        profile = user.get_profile()
    except:
        profile = None
    first = request.GET.get('first')
    if first == 'true' and not profile:
        new_profile = UserProfiles(user=user, avatar='avatar/default_face.gif')
        new_profile.save()
    profile = user.get_profile()
    
    if request.method == 'POST':
        profile.nickname = request.POST.get('nickname')
        profile.intro = request.POST.get('intro')
        profile.location = request.POST.get('location')
        profile.save()
        return HttpResponseRedirect('/%s/' % user.username)
    context = {}
    context['user'] = user
    context['profile'] = user.get_profile()
    return render_to_response('profiles/accounts_general.html', context)

@login_required  
def edit_avatar(request):
    user = request.user
    context = {}
    context['user'] = user
    if request.method == 'POST':
        new_avatar = request.FILES.get('avatar')
        filename = 'avatar_' + str(user.id)+'.jpg'
        if new_avatar:
            user.get_profile().avatar.save(filename, new_avatar, save=True)
        return HttpResponseRedirect('/profiles/')
    return render_to_response('profiles/accounts_avatar.html', context)

@login_required  
def edit_ability(request):
    user = request.user
    context = {}

    f_abilities = TabClass.objects.filter(tab_model_name='profiles')
    abilities = SubTabClass.objects.filter(parent_tab__tab_model_name='profiles')
    user_profile = user.get_profile()
    user_abilities = user_profile.ability.all()

    context['user'] = user
    context['f_abilities'] = f_abilities
    context['abilities'] = abilities
    context['user_abilities'] = user_abilities
    context['user_profile'] = user_profile

    if request.method == 'POST':
        new_abilities = request.POST.getlist('ability')
        user_profile.ability.clear()
        for na in new_abilities:
            e = SubTabClass.objects.get(pk=na)
            user_profile.ability.add(e)
        user_profile.save()
    return render_to_response('profiles/accounts_ability.html', context)
    
def watch_work(request, username):
    user= request.user
    the_user = User.objects.get(username=username)
    result = the_user.get_profile().share_work.all()
    context = {}
    context['user'] = user
    context['result'] = result
    context['the_user'] = the_user
    context['model'] = 'watch'
    return render_to_response('profiles/work_list.html', context)
    
def watch_work(request, username):
    user= request.user
    the_user = User.objects.get(username=username)
    result = the_user.get_profile().share_work.all()
    re = []
    for r in result:
        re.append(r.work)

    paginator = Paginator(re, 50) # Show 25 contacts per page
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
    context['user'] = user
    context['result'] = n
    context['the_user'] = the_user
    context['model'] = u'关注'
    return render_to_response('profiles/work_list.html', context)
    
def joint_work(request, username):
    user= request.user
    the_user = User.objects.get(username=username)
    context = {}
    in_work = []
    for m in Membership.objects.filter(user=the_user, status='Agr'):
        in_work.append(m.work)

    paginator = Paginator(in_work, 50) # Show 25 contacts per page
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
    
    context['result'] = n
    context['in_work'] = in_work
    context['user'] = user
    context['the_user'] = the_user
    context['model'] = u'参与'
    return render_to_response('profiles/work_list.html', context)
 
def re_work(request, username):
    user= request.user
    the_user = User.objects.get(username=username)
    context = {}
    model = request.GET.get('model')
    if model == '关注':
        result = the_user.get_profile().share_work.all()
        re = []
        for r in result:
            re.append(r.work)

        paginator = Paginator(re, 50) # Show 25 contacts per page
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
        context['user'] = user
        context['result'] = n
        context['the_user'] = the_user
        context['model'] = u'关注'
    if model == '参与':
        in_work = []
        for m in Membership.objects.filter(user=the_user, status='Agr'):
            in_work.append(m.work)

        paginator = Paginator(in_work, 50) # Show 25 contacts per page
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
        
        context['result'] = n
        context['in_work'] = in_work
        context['user'] = user
        context['the_user'] = the_user
        context['model'] = u'参与'
    return render_to_response('profiles/work_list.html', context)
    
    