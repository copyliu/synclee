# -*- coding: UTF-8 -*-
from django.core.cache import cache

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from synclee.profiles.models import UserProfiles, ShareWork
from synclee.notification import models as notification
from synclee.tweet.models import Tweet, TweetComment
from django.views.decorators.csrf import csrf_exempt
from synclee.notification.models import Notice
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.utils import simplejson
from operator import attrgetter
from itertools import chain
#simplejson

#@csrf_exempt
@login_required
def add_tweet(request):
    user = request.user
    req = simplejson.loads(request.raw_post_data)
    content = req['status']
    new_tweet = Tweet(user=user, content=content)
    new_tweet.save()
    object_type = ContentType.objects.get(name='tweet')
    object_id = new_tweet.id
    notification.send([user], "new_tweet", {"from_user": user, "tweet":new_tweet}, sender=user, object_type=object_type, object_id=object_id)
    return HttpResponse('...')
    
@login_required
def del_tweet(request):
    user = request.user
    tweet = Tweet.objects.get(pk=int(request.GET.get('tid')))
    if user == tweet.user:
        object_type = ContentType.objects.get(name='tweet')
        note = notification.Notice.objects.filter(object_type=object_type, object_id=tweet.id)
        note.delete()
        tweet.delete()
        return HttpResponse('...')
    return HttpResponse('...')
    
@login_required
def del_tweet_reply(request):
    user = request.user
    tweet_reply = request.GET.get('tid')
    if user == tweet_reply.user or user == tweet_reply.tweet.user:
        tweet_reply.delete()
        return HttpResponse('...')
    return HttpResponse('...')
    
#@csrf_exempt       
@login_required    
def reply_tweet(request):
    user = request.user
    req = simplejson.loads(request.raw_post_data)
    content = req['status']
    tweet = Tweet.objects.get(pk=int(request.GET.get('tweet_id')))
    object_type = ContentType.objects.get(name='tweet')
    object_id = tweet.id
    new_reply = TweetComment(tweet=tweet, user=user, content=content)
    new_reply.save()
    if user != tweet.user:
        notification.send([tweet.user], "new_reply", {"from_user": user, "object":tweet}, sender=user, object_type=object_type, object_id=object_id)
        tweet.user.get_profile().unread_notes += 1
        tweet.user.get_profile().save()
    return HttpResponse('...')
    
@login_required    
def refresh_tweet(request):
    user = request.user
    context = {}
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
    paginator = Paginator(result_list, 10) # Show 25 contacts per page
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
    
    context['notices'] = n
    return render_to_response('inc/timeline.html', context)
    
@login_required    
def refresh_person_tweet(request, username):
    user = request.user
    context = {}
    context['user'] = user
    the_user = User.objects.get(username=username)
    context['the_user'] = the_user
    exclude_type = ['new_reply', 'new_message', 'work_apply', 'work_deny', 'work_accept', 'work_invite', 'club_apply', 'club_deny', 'club_accept', 'club_invite', 'following', 'edit_text', 'edit_gallery']
    notices = Notice.objects.filter(sender=the_user).exclude(notice_type__label__in=exclude_type)
    paginator = Paginator(notices, 10) # Show 25 contacts per page
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        n = paginator.page(page)
    except (EmptyPage, InvalidPage):
        n = paginator.page(paginator.num_pages)
    
    context['notices'] = n
    return render_to_response('inc/person/timeline.html', context)