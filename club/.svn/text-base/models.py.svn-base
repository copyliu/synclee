# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from synclee.tab.models import SubTabClass, TabClass
from synclee.taggit.managers import TaggableManager
# Create your models here.

class Catalog(models.Model):
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50, blank=True)
    
    def __unicode__(self):
        return self.name

class Club(models.Model):
    name = models.CharField(max_length=50,unique=True)
    nickname = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    intro = models.TextField()
    founder = models.ForeignKey(User, related_name='own_club')
    manager = models.ManyToManyField(User, related_name='charge_club')
    cover = models.ImageField(upload_to='club/cover')
    members = models.ManyToManyField(User, through='ApplyClub', related_name='club_in')
    collected = models.PositiveIntegerField(default=0)
    
class ApplyClub(models.Model):
    MEMBER_STATUS = (
        (u'Inv', u'Invited'),
        (u'App', u'Applied'),
        (u'Agr', u'Agreed'),
    )
    user = models.ForeignKey(User)
    club = models.ForeignKey(Club)
    from_user = models.CharField(max_length=50)
    date_joined = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=MEMBER_STATUS)
    reason = models.TextField(default='I Love U!')
    
class Project(models.Model):
    name = models.CharField(max_length=50)
    cover = models.ImageField(blank=True, upload_to='cover', default='cover/default.jpg')
    club = models.ForeignKey(Club, related_name='project', null=True)
    founder = models.ForeignKey(User, related_name='own_pro')
    members = models.ManyToManyField(User, related_name='in_project')
    date = models.DateTimeField(auto_now_add=True)
    catalog = models.ForeignKey(Catalog, related_name='project')
    tab = models.ManyToManyField(SubTabClass, limit_choices_to={'parent_tab__tab_model_name':'project'}, related_name='project')
    tags = TaggableManager()
    support = models.IntegerField(default=0) #支持
    collected = models.IntegerField(default=0) #关注
    closed = models.BooleanField(default=False)
    intro = models.TextField()
