# -*- coding: utf-8 -*-

from django.contrib import admin
from synclee.chapter.models import *
from django import forms


class SampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }

    class Media:
        js = ('/img/ckeditor/ckeditor.js',) # The , at the end of this list IS important.
        
class TextChapterAdmin(admin.ModelAdmin):
    list_display = ['title']
class GalleryChapterAdmin(admin.ModelAdmin):
    list_display = ['title']
class TextSectionAdmin(admin.ModelAdmin):
    list_display = ['title']
class GallerySectionAdmin(admin.ModelAdmin):
    list_display = ['title']
class ChapterCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'work', 'text', 'gallery']


admin.site.register(TextChapter, TextChapterAdmin)
admin.site.register(TextSection, TextSectionAdmin)
admin.site.register(GalleryChapter, GalleryChapterAdmin)
admin.site.register(GallerySection, GallerySectionAdmin)
admin.site.register(ChapterComment, ChapterCommentAdmin)
admin.site.register(UpdateHistory)


__author__ = 'Administrator'
  