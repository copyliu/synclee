# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from notification.models import Notice
from works.models import Work

def home(request):
    works = Work.objects.all()
    hot_works = Work.objects.all()
    ctx = {
        'works' : works,
        'hot_works' : hot_works
    }
    return TemplateResponse(request, 'home.html', ctx)

def unread(request):
    notices = Notice.objects.notices_for(request.user).filter(unseen=1).count()
    if notices:
        return HttpResponse(notices)
    else:
        return HttpResponse(0)

def server_error(request, template_name='500.html'):
    """
    A simple 500 handler so we get media
    """
    r = render_to_response(template_name,
        context_instance = RequestContext(request)
    )
    r.status_code = 500
    return r

def server_error_404(request, template_name='404.html'):
    """
    A simple 404 handler so we get media
    """
    r =  render_to_response(template_name,
        context_instance = RequestContext(request)
    )
    r.status_code = 404
    return r