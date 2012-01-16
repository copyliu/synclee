# -*- coding: UTF-8 -*-
from django.db.transaction import commit_on_success
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
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

@commit_on_success
#@login_required  
def add_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            intro = form.cleaned_data['intro']
            work = Work.objects.create(name=name, intro=intro)
            work.save()
            #uploaded = request.FILES.get('cover', '')
            #catalog_id = request.POST.get('catalog_id')
            
        #if uploaded:
        #    work.cover.save('work_%s_cover.jpg' % work.id, ContentFile(uploaded.read()), save=True)
        #object_type = ContentType.objects.get(name='work')
        #object_id = new_work.id
        #notification.send([user], "new_work", {"from_user": user, "work":new_work}, sender=user, object_type=object_type, object_id=object_id)
            return HttpResponseRedirect('/works/write_work/%s' % work.id)
        else:
            return TemplateResponse(request, 'works/add_work.html', {'form': form})

    else:
        form = WorkForm()
        return TemplateResponse(request, 'works/add_work.html', {'form': form})

def write_work(request, work_id):
    work = Work.objects.get(pk=int(work_id))
    return TemplateResponse(request, 'works/write_work.html', {'work' : work})