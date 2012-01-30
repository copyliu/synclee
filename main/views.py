# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse

from works.models import Work

def home(request):
    works = Work.objects.all()
    return TemplateResponse(request, 'home.html', {'works': works})
