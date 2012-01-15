# -*- coding: utf-8 -*-

from django.contrib import admin
from synclee.work.models import *
from django import forms


class SampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

    class Media:
        js = ('/img/ckeditor/ckeditor.js',) # The , at the end of this list IS important.
        
class WorkAdmin(admin.ModelAdmin):
    list_display = ['name', 'catalog']

admin.site.register(Work, WorkAdmin)
admin.site.register(Value)
admin.site.register(Membership)
admin.site.register(Option)
admin.site.register(OptionChoice)
admin.site.register(Issue)







__author__ = 'Administrator'
  