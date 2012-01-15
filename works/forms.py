# -*- coding=utf-8 -*-

from django import forms
#from django.contrib.auth import authenticate, login
#from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.models import User
#from django.forms.util import ErrorList
#from django.shortcuts import redirect, HttpResponse


class WorkForm(forms.Form):
    name = forms.CharField(error_messages = {'required': u'名称不能为空'}, max_length = 30)
    intro = forms.CharField(required = False)
    catalog = forms.CharField(error_messages = {'required':u'这个字段是必填的'}, required = True)
    