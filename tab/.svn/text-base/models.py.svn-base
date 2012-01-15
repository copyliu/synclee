# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.


class TabClass(models.Model):
    tab_name = models.CharField(max_length=20, unique=True)
    tab_model_name = models.CharField(max_length=20)
    
    def get_icon(self):
        if self.tab_name == u'写手':
            return 'litera lv1'
        if self.tab_name == u'画师':
            return 'illust lv2'
        if self.tab_name == u'程序员':
            return 'prog lv3'
        if self.tab_name == u'设计美工':
            return 'web lv4'
        if self.tab_name == u'音乐制作':
            return 'music lv4'
        else:
            return 'shui lv5'

    
class SubTabClass(models.Model):
    sub_name = models.CharField(max_length=20, unique=True)
    parent_tab = models.ForeignKey(TabClass, related_name='subtab')
    
    def __unicode__(self):
        return self.sub_name