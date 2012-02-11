# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

from works.models import Work

class UserProfiles(models.Model):
    user = models.ForeignKey(User, related_name='profile')
    avatar = ThumbnailerImageField(upload_to='avatar', default='avatar/default_avatar.jpg', resize_source=dict(size=(200, 200), crop='big'),)
    website = models.URLField(blank = True)
    intro = models.TextField()
    location = models.CharField(max_length = 50, blank = True)
    true_name = models.CharField(max_length = 14, blank = True)
    email = models.EmailField()

def create_user_profile(sender = None, instance = None, created = False, **kwargs):
    if created:
        UserProfiles.objects.create(user=instance)
        UserSkills.objects.create(user=instance, skill='write')
        UserSkills.objects.create(user=instance, skill='paint')
        UserSkills.objects.create(user=instance, skill='onlook')
        
models.signals.post_save.connect(create_user_profile, sender = User)

SKILL_CHOICES = (
    ('write', u'写手'),
    ('paint', u'画师'),
    ('design', u'设计美工'),
    ('prog', u'程序员'),
    ('music', u'音乐制作'),
    ('onlook',u'围观'),
    ('_other', u'其他'),
)

class UserSkills(models.Model):
    user = models.ForeignKey(User, related_name='skills')
    skill = models.CharField(max_length=8, choices=SKILL_CHOICES)
    exp = models.IntegerField(default = 0)
    today_exp = models.IntegerField(default = 0)

class AccountTempPassword(models.Model):
    user = models.ForeignKey(User, related_name='tmp_psw')
    tmp_psw = models.CharField(max_length = 20)
    datetime = models.DateTimeField(auto_now_add = True)

class Invitation(models.Model):
    INVITE_CHOICES = (
        (u'noanswer', u'未响应'),
        (u'goingon', u'申请中'),
        (u'accept', u'已接受'),
        (u'reject', u'已拒绝')
    )
    work = models.ForeignKey(Work, related_name='invitaion')
    invited = models.ForeignKey(User, related_name='invited')
    skill = models.CharField(max_length=8, choices=SKILL_CHOICES)
    reason = models.CharField(max_length = 300)
    invite_status = models.CharField(max_length=8, choices=INVITE_CHOICES)
