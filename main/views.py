# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.response import TemplateResponse

def home(request):
    return TemplateResponse(request, 'home.html')
