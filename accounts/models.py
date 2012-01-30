# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from easy_thumbnails.fields import ThumbnailerImageField

from accounts.skills import SKILL_CHOICES

class UserProfiles(models.Model):
    user = models.ForeignKey(User, related_name='profile')
    avatar = ThumbnailerImageField(upload_to='avatar', default='avatar/default_avatar.jpg', resize_source=dict(size=(200, 200), crop='big'),)
    website = models.URLField(blank = True)
    intro = models.TextField()
    location = models.CharField(max_length = 50, blank = True)
    true_name = models.CharField(max_length = 14, blank = True)
    email = models.EmailField()
    
    #技能
    skill = models.PositiveIntegerField(default = 0)
    #权限
    #作品
    #关注作品
    #参与作品
    #。。。

def create_user_profile(sender = None, instance = None, created = False, **kwargs):
    if created:
        UserProfiles.objects.create(user = instance)
   
models.signals.post_save.connect(create_user_profile, sender = User)

class UserSkills(models.Model):
    user = models.ForeignKey(User, related_name='skills')
    skill = models.CharField(max_length=8, choices=SKILL_CHOICES)
    exp = models.IntegerField(default = 0)
    today_exp = models.IntegerField(default = 0)

class AccountTempPassword(models.Model):
    user = models.ForeignKey(User, related_name='tmp_psw')
    tmp_psw = models.CharField(max_length = 20)
    datetime = models.DateTimeField(auto_now_add = True)