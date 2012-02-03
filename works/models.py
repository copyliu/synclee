# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
#from synclee.club.models import Club, Project, Catalog
#from synclee.tab.models import SubTabClass, TabClass
from taggit.managers import TaggableManager
from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.comments.moderation import CommentModerator, moderator

class TimeLines(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    instance = generic.GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add = True)


class Work(models.Model):
    PRIVACY_CHOICES = (
        (u'Pub', u'公开'),
        (u'Fri', u'好友可见'),
        (u'Pri', u'私人'),
    )
    name = models.CharField(max_length=48)
    cover = ThumbnailerImageField(
        blank=True,
        upload_to='cover',
        resize_source=dict(size=(300, 300), crop='smart'),
        default='cover/default_cover.gif'
    )
    author = models.ForeignKey(User)
    #project = models.ForeignKey(Project, related_name='work', null=True)
    #founder = models.ForeignKey(User, related_name='own_work')
    #members = models.ManyToManyField(User, through='Membership', related_name='in_work')
    follower = models.ManyToManyField(User, related_name='follow')
    created = models.DateTimeField(auto_now_add=True)
    #privacy = models.CharField(max_length=3, choices=PRIVACY_CHOICES)
    #catalog = models.ForeignKey(Catalog, related_name='work')
    #tab = models.ManyToManyField(SubTabClass, limit_choices_to={'parent_tab__tab_model_name':'work'}, related_name='work')
    tags = TaggableManager()

    closed = models.BooleanField(default=False)
    intro = models.TextField()
    
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