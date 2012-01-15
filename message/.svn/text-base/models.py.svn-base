# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):
    MESSAGE_STATUS = (
        (u'Unread', u'未读'),
        (u'Read', u'已读'),
    )
    sender = models.ForeignKey(User, related_name="sent_mail")
    receiver = models.ForeignKey(User, related_name="received_mail")
    title = models.CharField(max_length=50)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=MESSAGE_STATUS)
    
    def get_sender():
        return sender
    
    def get_receiver():
        return receriver
    
    def is_read():
        if status == 'Unread':
            return False
        else:
            return True