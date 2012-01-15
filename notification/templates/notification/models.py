# -*- coding: UTF-8 -*-

from django.db import models
from synclee.club.models import Club, Project
from synclee.work.models import Work
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
# Create your models here.

class TextChapter(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey(User, related_name='text_chapter')
    abstract = models.TextField(blank=True)
    from_work = models.ForeignKey(Work, related_name='sync_text', null=True)
    work = models.ForeignKey(Work, related_name='text_chapter', null=True)
    club = models.ForeignKey(Club, related_name='text_chapter', null=True)
    
    def is_club_chapter(self):
        if club == None:
            return False
        else:
            return True
        
    def get_absolute_url(self):
        if self.work:
            return '/work/%s/text/?text_id=%s' % (self.work.id, self.id)
        if self.club:
            return '/club/%s/text/?text_id=%s' % (self.work.name, self.id)
        
    def get_reply_url(self):
        return '/work/%s/reply/?text_id=%s' % (work.id, self.id)
        
class TextSection(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey(User, related_name='text_section')
    chapter = models.ForeignKey(TextChapter, related_name='section')
    content = models.TextField()
    
class GalleryChapter(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey(User, related_name='gallery_chapter')
    abstract = models.TextField(blank=True)
    from_work = models.ForeignKey(Work, related_name='sync_gallery', null=True)
    work = models.ForeignKey(Work, related_name='gallery_chapter', null=True)
    club = models.ForeignKey(Club, related_name='gallery_chapter', null=True)
    project = models.ForeignKey(Project, related_name='gallery_chapter', null=True)
    
    def is_club_chapter(self):
        if club == None:
            return False
        else:
            return True
        
    def is_project_chapter(self):
        if project == None:
            return False
        else:
            return True

    def get_absolute_url(self):
        return '/work/%s/gallery/?gallery_id=%s' % (work.id, self.id)
        
    def get_reply_url(self):
        return '/work/%s/reply/?gallery_id=%s' % (work.id, self.id)
    
class GallerySection(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey(User, related_name='gallery_section')
    chapter = models.ForeignKey(GalleryChapter, related_name='section')
    picture = models.ImageField(upload_to='picture')
    
class TextModerator(CommentModerator):
    email_notification = False
    enable_field = 'enable_comments'
    
class GalleryModerator(CommentModerator):
    email_notification = False
    enable_field = 'enable_comments'
    
class UpdateHistory(models.Model):
    work = models.ForeignKey(Work, related_name='history')
    mode = models.CharField(max_length=10)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    text = models.ForeignKey(TextChapter, null=True)
    gallery = models.ForeignKey(GalleryChapter, null=True)
    chapter_name = models.CharField(max_length=100, blank=True)
    
    def get_history_message(self):
        if mode == u'删除':
            if text:
                url = text.get_absolute_url()
            elif gallery:
                url = gallery.get_absolute_url()
            name = chapter_name
            return '%s %s' % (mode, name)
        else:
            if text:
                url = text.get_absolute_url()
                name = text.name
            elif gallery:
                url = gallery.get_absolute_url()
                name = text.name
            return '%s <a href="%s">%s</a>' % (mode, url, name)
            
class ChapterComment(models.Model):
    work = models.ForeignKey(Work, related_name='comment')
    text = models.ForeignKey(TextChapter, related_name='comment', null=True)
    gallery = models.ForeignKey(GalleryChapter, related_name='comment', null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    
#moderator.register(TextChapter, TextModerator)
#moderator.register(GalleryChapter, GalleryModerator)