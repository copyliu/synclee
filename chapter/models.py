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
        if self.club == None:
            return False
        else:
            return True
        
    def get_absolute_url(self):
        if not self.is_club_chapter():
            return '/work/%s/text/?text_id=%s' % (self.work.id, self.id)
        else:
            return '/club/%s/text/?text_id=%s' % (self.club.name, self.id)
        
    def get_reply_url(self):
        if not self.is_club_chapter():
            return '/work/%s/reply/?text_id=%s' % (self.work.id, self.id)
        else:
            return '/club/%s/reply/?text_id=%s' % (self.club.name, self.id)
            
    def get_first(self):
        if self.section.all().count() > 0:
            return self.section.all()[0].id
        else:
            return ""
        
    def get_work_id(self):
        return self.work.id
    
    def get_refresh_url(self):
        return '/work/%s/refresh_comment/?page=1&text_id=%s&gallery_id=' % (self.work.id, self.id)
        
    def get_text_id(self):
        return self.id
    
    def get_gallery_id(self):
        return None
    
    def get_name(self):
        return self.title
    
    def __unicode__(self):
        return self.title
    
class TextSection(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey(User, related_name='text_section')
    chapter = models.ForeignKey(TextChapter, related_name='section')
    content = models.TextField()
    
    def __unicode__(self):
        return self.title
    
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
        if self.club == None:
            return False
        else:
            return True
        
    def is_project_chapter(self):
        if self.project == None:
            return False
        else:
            return True
        
    def get_absolute_url(self):
        if not self.is_club_chapter():
            return '/work/%s/gallery/?gallery_id=%s' % (self.work.id, self.id)
        else:
            return '/club/%s/gallery/?gallery_id=%s' % (self.club.name, self.id)
        
    def get_reply_url(self):
        if not self.is_club_chapter():
            return '/work/%s/reply/?gallery_id=%s' % (self.work.id, self.id)
        else:
            return '/club/%s/reply/?gallery_id=%s' % (self.club.name, self.id)
            
    def get_first(self):
        if self.section.all().count() > 0:
            return self.section.all()[0].id
        else:
            return ""
        
    def get_work_id(self):
        return self.work.id
    
    def get_refresh_url(self):
        return '/work/%s/refresh_comment/?page=1&text_id=&gallery_id=%s' % (self.work.id, self.id)
        
    def get_text_id(self):
        return None
    
    def get_gallery_id(self):
        return self.id
    
    def get_name(self):
        return self.title
    
    def __unicode__(self):
        return self.title

    
class GallerySection(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey(User, related_name='gallery_section')
    chapter = models.ForeignKey(GalleryChapter, related_name='section')
    picture = models.ImageField(upload_to='picture', default="/p0.jpg")
    content = models.TextField()
    
    def __unicode__(self):
        return self.title
    
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
        if self.mode == 'remove':
            if self.text:
                url = self.text.get_absolute_url()
            elif self.gallery:
                url = self.gallery.get_absolute_url()
            name = self.chapter_name
            return u'删除了 <del>%s</del>' % name
        elif self.mode == 'modify':
            if self.text:
                url = self.text.get_absolute_url()
                name = self.text.title
            elif self.gallery:
                url = self.gallery.get_absolute_url()
                name = self.gallery.title
            return u'修改了 <a href="%s">%s</a>' % (url, name)
        else:
            if self.text:
                url = self.text.get_absolute_url()
                name = self.text.title
                last_url = u'增加了 <ins><a href="%s">%s</a></ins>' % (url, name)
            elif self.gallery:
                url = self.gallery.get_absolute_url()
                name = self.gallery.title
                last_url = u'增加了 <ins><a href="%s">%s</a></ins>' % (url, name)
            return last_url
            
class ChapterComment(models.Model):
    work = models.ForeignKey(Work, related_name='comment')
    text = models.ForeignKey(TextChapter, related_name='comment', null=True)
    gallery = models.ForeignKey(GalleryChapter, related_name='comment', null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    
#moderator.register(TextChapter, TextModerator)
#moderator.register(GalleryChapter, GalleryModerator)