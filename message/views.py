# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from synclee.message.models import Message

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from synclee.notification import models as notification

def inbox(request):
    context = {}
    user = request.user
    context['user'] = user
    if user.is_authenticated():
        mails = user.received_mail.all().order_by('-date')
        context['mails'] = mails
        return render_to_response('message/inbox.html', context)
    else:
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
        
def sent(request):
    context = {}
    user = request.user
    context['user'] = user
    if user.is_authenticated():
        mails = user.sent_mail.all().order_by('-date')
        context['mails'] = mails
        return render_to_response('message/sent.html', context)
    else:
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)


def write_message(request):
    context = {}
    user = request.user
    context['user'] = user
    receiver = User.objects.get(username=request.GET.get('username'))
    context['receiver'] = receiver
    if user.is_authenticated():
        if request.method == 'POST':
            sender = user
            title = request.POST.get('title')
            body = request.POST.get('body')
            new_message = Message(sender=sender, receiver=receiver, title=title, body=body, status='Unread')
            new_message.save()
            receiver.get_profile().unread_message += 1
            receiver.get_profile().save()
            notification.send([receiver], "new_message", {"from_user": user, "mail":new_message}, sender=user)
            return HttpResponseRedirect('/message/sent/')
        else:
            return render_to_response('message/write_message.html', context)
    else:
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)

def view_message(request):
    context = {}
    user = request.user
    context['user'] = user
    mail_id = request.GET.get('mail_id')
    if user.is_authenticated():
        try:
            mail = Message.objects.get(id=mail_id)
        except:
            return render_to_response('error.html', {'error':u'错误的邮件ID'})
        if user == mail.receiver or user == mail.sender :
            context['mail'] = mail
            if not mail.status == 'Read':
                if user == mail.receiver:
                    user.get_profile().unread_message -= 1
                    user.get_profile().save()
                mail.status = 'Read'
                mail.save()
            return render_to_response('message/view_message.html', context)
        else:
            return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    else:
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)