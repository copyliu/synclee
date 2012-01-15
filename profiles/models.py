# -*- coding: UTF-8 -*-

from django.db import models
from synclee.work.models import *
from synclee.chapter.models import *
from synclee.club.models import *
from synclee.message.models import Message
from synclee.notification.models import Notice
from synclee.taggit.managers import TaggableManager
# Create your models here.

class UserProfiles(models.Model):
    user = models.ForeignKey(User, related_name='profile')
    avatar = models.ImageField(upload_to='avatar', default='/1.jpg')
    nickname = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    intro = models.TextField()
    location = models.CharField(max_length=50)
    available = models.IntegerField(default=0)
    ability = models.ManyToManyField(SubTabClass, limit_choices_to={'parent_tab__tab_model_name':'profiles'})
    tags = TaggableManager()
    shares = models.ManyToManyField(Work, through='ShareWork')

    unread_notes = models.PositiveIntegerField(default=0)
    unread_message = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    
    def get_name(self):
        return self.nickname
    
    def get_absolute_url(self):
        return '/%s/' % self.user.username
    
    def get_cover(self):
        return self.avatar
    
    def get_f_ability(self):
        the_user_abilities = self.ability.all()
        f_ability = []
        for tua in the_user_abilities:
            f_ability.append(tua.parent_tab)
        f_ability = list(set(f_ability))
        return f_ability
    
    def get_share_work_id(self):
        wlist = []
        tlist = []
        glist = []
        for w in self.share_work.all():
            wlist.append(w.work.id)
            for t in w.work.text_chapter.all():
                tlist.append(t.id)
            for g in w.work.text_chapter.all():
                glist.append(g.id)
        context = {}
        context['wlist'] = wlist
        context['tlist'] = tlist
        context['glist'] = glist
        return context
    
    def get_unread_message(self):
        mes = Message.objects.filter(receiver=self.user, status='unread').count()
        return mes
        
    def get_unread_app(self):
        return Notice.objects.filter(recipient=self.user, notice_type__label='work_apply', unseen=True).count()
        #return Notice.objects.unseen_count_for(self, notice_type='work_apply')
    
    def get_unread_agr(self):
        return Notice.objects.filter(recipient=self.user, notice_type__label='work_accept', unseen=True).count()
        #return Notice.objects.unseen_count_for(self, notice_type='work_agr')
    
    def get_unread_inv(self):
        return Notice.objects.filter(recipient=self.user, notice_type__label='work_invite', unseen=True).count()
        #return Notice.objects.unseen_count_for(self, notice_type='work_invtie')
        
    def get_unread_rep(self):
        return Notice.objects.filter(recipient=self.user, notice_type__label='new_reply', unseen=True).count()

class ShareWork(models.Model):
    user_profile = models.ForeignKey(UserProfiles, related_name='share_work')
    work = models.ForeignKey(Work, related_name='be_shared')
    reason = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date"]