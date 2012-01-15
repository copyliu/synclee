# Create your views here.
# -*- coding: UTF-8 -*-
# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

def about(request):
    user = request.user
    context = {}
    context['user'] = user
    return render_to_response('general/about.shtml', context)
    
def help(request):
    user = request.user
    context = {}
    context['user'] = user
    return render_to_response('general/help.shtml', context)