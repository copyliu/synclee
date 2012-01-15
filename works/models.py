# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
#from synclee.club.models import Club, Project, Catalog
#from synclee.tab.models import SubTabClass, TabClass
from taggit.managers import TaggableManager
from django.contrib.comments.moderation import CommentModerator, moderator

class Work(models.Model):
    PRIVACY_CHOICES = (
        (u'Pub', u'公开'),
        (u'Fri', u'好友可见'),
        (u'Pri', u'私人'),
    )
    name = models.CharField(max_length=48)
    cover = models.ImageField(blank=True, upload_to='cover', default='cover/default_cover.gif')
    #project = models.ForeignKey(Project, related_name='work', null=True)
    #founder = models.ForeignKey(User, related_name='own_work')
    #members = models.ManyToManyField(User, through='Membership', related_name='in_work')
    date = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=3, choices=PRIVACY_CHOICES)
    #catalog = models.ForeignKey(Catalog, related_name='work')
    #tab = models.ManyToManyField(SubTabClass, limit_choices_to={'parent_tab__tab_model_name':'work'}, related_name='work')
    tags = TaggableManager()
    support = models.IntegerField(default=0) #支持
    collected = models.IntegerField(default=0) #关注
    push = models.IntegerField(default=0) #催稿
    #push_today = models.IntegerField(default=0)
    puship = models.ManyToManyField(User, related_name='pushed')
    closed = models.BooleanField(default=False)
    intro = models.TextField()
    