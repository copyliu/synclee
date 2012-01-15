# -*- coding: utf-8 -*-

from django.contrib import admin
from synclee.profiles.models import *
from django import forms


class SampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

    class Media:
        js = ('/img/ckeditor/ckeditor.js',) # The , at the end of this list IS important.

admin.site.register(UserProfiles)



__author__ = 'Administrator'
  