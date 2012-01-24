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
    #权限
    #作品
    #关注作品
    #参与作品
    #。。。
