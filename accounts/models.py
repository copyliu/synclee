# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

from works.models import Work

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile')
    avatar = ThumbnailerImageField(upload_to='avatar', default='avatar/default_avatar.jpg', resize_source=dict(size=(200, 200), crop='big'),)
    website = models.URLField(blank = True)
    intro = models.TextField()
    location = models.CharField(max_length = 50, blank = True)
    true_name = models.CharField(max_length = 14, blank = True)
    email = models.EmailField()

def create_user_profile(sender = None, instance = None, created = False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Skill.objects.create(user=instance, skill='word')
        Skill.objects.create(user=instance, skill='image')
        Skill.objects.create(user=instance, skill='other')
        
models.signals.post_save.connect(create_user_profile, sender = User)

SKILL_CHOICES = (
    ('word', u'写手'),
    ('image', u'画师'),
#    ('design', u'设计美工'),
#    ('prog', u'程序员'),
#    ('music', u'音乐制作'),
#    ('onlook',u'围观'),
    ('other', u'其他'),
)

class Skill(models.Model):
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
        (u'accept', u'已接受'),
        (u'reject', u'已拒绝')
    )
    work = models.ForeignKey(Work, related_name='invitaion')
    invited = models.ForeignKey(User, related_name='invited')
    role = models.CharField(max_length=8, choices=SKILL_CHOICES)
    reason = models.CharField(max_length = 300)
    invite_status = models.CharField(max_length=8, choices=INVITE_CHOICES)
