# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from synclee.club.models import Club, Project, Catalog
from synclee.tab.models import SubTabClass, TabClass
from synclee.taggit.managers import TaggableManager
from django.contrib.comments.moderation import CommentModerator, moderator
# Create your models here.

class Work(models.Model):
    PRIVACY_CHOICES = (
        (u'Pub', u'公开'),
        (u'Fri', u'好友可见'),
        (u'Pri', u'私人'),
    )
    name = models.CharField(max_length=50)
    cover = models.ImageField(blank=True, upload_to='cover', default='cover/default_cover.gif')
    project = models.ForeignKey(Project, related_name='work', null=True)
    founder = models.ForeignKey(User, related_name='own_work')
    members = models.ManyToManyField(User, through='Membership', related_name='in_work')
    date = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=3, choices=PRIVACY_CHOICES)
    catalog = models.ForeignKey(Catalog, related_name='work')
    tab = models.ManyToManyField(SubTabClass, limit_choices_to={'parent_tab__tab_model_name':'work'}, related_name='work')
    tags = TaggableManager()
    support = models.IntegerField(default=0) #支持
    collected = models.IntegerField(default=0) #关注
    push = models.IntegerField(default=0) #催稿
    push_today = models.IntegerField(default=0)
    puship = models.ManyToManyField(User, related_name='pushed')
    closed = models.BooleanField(default=False)
    intro = models.TextField()
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/work/%s/' % self.id
    
    def get_reply_url(self):
        return '/work/%s/reply/' % self.id
    
    def get_members(self):
        members = []
        for m in Membership.objects.filter(work=self, status='Agr'):
            members.append(m.user)
        return members
        
    def get_active_issue(self):
        return self.issue.filter(status=1)
        
    def get_name(self):
        return self.name
    
    def get_cover(self):
        return self.cover
    
    def get_work_id(self):
        return self.id
    
    def get_refresh_url(self):
        return '/work/%s/refresh_comment/' % self.id
    
    def get_text_id(self):
        return None
    
    def get_gallery_id(self):
        return None
    
class Membership(models.Model):
    MEMBER_STATUS = (
        (u'Inv', u'Invited'),
        (u'App', u'Applied'),
        (u'Agr', u'Agreed'),
    )
    user = models.ForeignKey(User)
    work = models.ForeignKey(Work)
    from_user = models.CharField(max_length=50)
    date_joined = models.DateField(auto_now_add=True)
    ability = models.ForeignKey(SubTabClass, blank=True, default=None, null=True)
    status = models.CharField(max_length=10, choices=MEMBER_STATUS)
    reason = models.TextField(default='I Love U!')
    
class Option(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, default='text')
    catalog = models.ForeignKey(Catalog, related_name='option')
    
class OptionChoice(models.Model):
    option = models.ForeignKey(Option, related_name='choice')
    name = models.CharField(max_length=50)
    
class Value(models.Model):
    work = models.ForeignKey(Work)
    option = models.ForeignKey(Option)
    value = models.TextField(default=0)
    
class Issue(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    auther = models.ForeignKey(User, related_name='issue')
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    work = models.ForeignKey(Work, related_name='issue')
    
    def get_absolute_url(self):
        return '/work/%s/issues/%s' % (self.work.id, self.id)
        
    def is_open(self):
        if self.status:
            return True
        else:
            return False
        
class IssueModerator(CommentModerator):
    email_notification = False
    enable_field = 'enable_comments'
    
#moderator.register(Issue, IssueModerator)