# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
#from synclee.club.models import Club, Project, Catalog
#from synclee.tab.models import SubTabClass, TabClass

from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.comments.moderation import CommentModerator, moderator

import os, settings

class TimeLine(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    instance = generic.GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add = True)

def get_image_path(instance, filename):
    return os.path.join('works', str(instance.id), filename)
class Work(models.Model):
    PRIVACY_CHOICES = (
        (u'Pub', u'公开'),
        (u'Fri', u'好友可见'),
        (u'Pri', u'私人'),
    )
    name = models.CharField(max_length=48)
    cover = ThumbnailerImageField(
        blank=True,
        upload_to=get_image_path,
        resize_source=dict(size=(360, 268), crop='smart'),
        default='no_cover.gif'
    )
    author = models.ForeignKey(User)
    category = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    isprivate = models.BooleanField(default=False)
    intro = models.TextField(blank=True)
    
    follower = models.ManyToManyField(User, related_name='follow')
    
    def aver_score(self):
        return WorkScore.objects.filter(work=self).aggregate(average_score=models.Avg('score'))['average_score'] or 0
#def work_event(sender = None, instance = None, created = False, **kwargs):
#    if created:
#        TimeLines.objects.create(user = instance.author, event = instance)
#   
#models.signals.post_save.connect(work_event, sender = Work)
 
class Action(models.Model):
    ACTION_CHOICES = (
        ('support', u'支持'),
        ('follow', u'关注'), #TODO : Power by django-follow
        ('push', u'催稿')
    )
    user = models.ForeignKey(User)
    action = models.CharField(max_length=8, choices=ACTION_CHOICES)
    work = models.ForeignKey(Work)
    #push_today = models.IntegerField(default=0)

class Element(models.Model):
    CATEGORY_CHOICE = (
        ('text', u'文字'),
        ('image', u'图片'),
        ('line', u'分割线')
    )
    category = models.CharField(max_length=8, choices=CATEGORY_CHOICE)
    title = models.CharField(max_length=64, blank=True)
    content = models.TextField()
    work = models.ForeignKey(Work)
    
def element_event(sender = None, instance = None, created = False, **kwargs):
    if created:
        TimeLines.objects.create(user = instance.work.author, instance = instance)
   
models.signals.post_save.connect(element_event, sender = Element)

class WorkScore(models.Model):
    work = models.ForeignKey(Work)
    user = models.ForeignKey(User)
    score = models.PositiveSmallIntegerField(default = 0)

class WorkHistory(models.Model):
    work = models.ForeignKey(Work)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']