# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User
# Create your models here.
class UserProfiles(models.Model):
    user = models.ForeignKey(User, related_name='profile')
    avatar = models.ImageField(upload_to='avatar', default='avatar/default_avatar')
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