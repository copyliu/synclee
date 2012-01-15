# -*- coding: UTF-8 -*-
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from .models import Work
from .forms import WorkForm

from django.core.paginator import Paginator, InvalidPage, EmptyPage

import string, random
from django.utils import simplejson

PRIVACY_CHOICES = (
        (u'Pub', u'公开'),
        (u'Fri', u'好友可见'),
        (u'Pri', u'私人'),        
    )


#@login_required  
def add_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
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
    else:
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
    return render_to_response('work/add_work.shtml', context)
