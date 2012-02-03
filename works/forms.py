# -*- coding=utf-8 -*-

from django import forms
#from django.contrib.auth import authenticate, login
#from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.models import User
#from django.forms.util import ErrorList


class WorkForm(forms.Form):
    name = forms.CharField(error_messages = {'required': u'名称不能为空'}, max_length = 30)
    intro = forms.CharField(required = False)
    category = forms.CharField(required = False)
    isprivate = forms.IntegerField(required = False)
    
    def clean_isprivate(self):
        if 'isprivate' in self.cleaned_data:
            if self.cleaned_data['isprivate']:
                self.cleaned_data['isprivate'] = 1
            else:
                self.cleaned_data['isprivate'] = 0
            return self.cleaned_data['isprivate']