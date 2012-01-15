# -*- coding: UTF-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Avg, Max, Min, Count

from synclee.work.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def search(request):
    user = request.user
    context = {}
    context['user'] = user
    query = request.GET.get('query')
    try:
        order = request.GET.get('order')
        if order == 'release':
            result = Work.objects.all().filter(privacy='Pub').order_by('-date')
        elif order == 'support':
            result = Work.objects.all().filter(privacy='Pub').order_by('-push')
        elif order == 'watchers':
            result = Work.objects.all().filter(privacy='Pub').order_by('-collected')
        elif order == 'update':
            result = Work.objects.all().filter(privacy='Pub').order_by('-date')
        elif order == 'comment':
            result = Work.objects.annotate(num_comment=Count('comment')).filter(privacy='Pub').order_by('-num_comment')
        else:
            result = Work.objects.all().filter(privacy='Pub').order_by('-date')
    except:
        order = ""
        result = Work.objects.all().filter(privacy='Pub').order_by('-date')
    try:
        username = request.GET.get('author')
        if username:
            users = User.objects.filter(profile__nickname=username)
            result = result.filter(founder__in=users)
    except:
        username = ""
        result = result
    try:
        catalog = request.GET.get('catalog')
        if catalog:
            result = result.filter(catalog=Catalog.objects.get(label=catalog))
    except:
        catalog = None
        result = result
    
    result = result.filter(name__icontains=query)
    paginator = Paginator(result, 50) # Show 25 contacts per page
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
    context['catalog'] = catalog
    context['username'] = username
    context['order'] = order
    context['query'] = query
    return render_to_response('search/search.shtml', context)

def refresh_search(request):
    user = request.user
    context = {}
    context['user'] = user
    query = request.GET.get('query')
    result = Work.objects.filter(name__icontains=query)
    try:
        username = request.GET.get('author')
        if username:
            users = User.objects.filter(profile__nickname=username)
            result = result.filter(founder__in=users)
    except:
        username = ""
        result = result
    try:
        catalog = request.GET.get('catalog')
        if catalog:
            result = result.filter(catalog=Catalog.objects.get(label=catalog))
    except:
        catalog = None
        result = result
    try:
        order = request.GET.get('order')
        if order == 'release':
            result = result.order_by('-date')
        if order == 'support':
            result = result.order_by('-push')
        if order == 'watchers':
            result = result.order_by('-collected')
        if order == 'update':
            result = result.order_by('-date')
        else:
            result = result
    except:
        order = ""
        result = result.order_by('-date')
    paginator = Paginator(result, 50) # Show 25 contacts per page
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
    context['catalog'] = catalog
    context['username'] = username
    context['order'] = order
    context['query'] = query
    return render_to_response('inc/project-list/list.shtml', context)