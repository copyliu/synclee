# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse

from notification.models import Notice
from works.models import Work

def home(request):
    works = Work.objects.all()
    return TemplateResponse(request, 'home.html', {'works': works})

def unread(request):
    notices = Notice.objects.notices_for(request.user).filter(unseen=1).count()
    if notices:
        return HttpResponse(notices)
    else:
        return HttpResponse(0)
    