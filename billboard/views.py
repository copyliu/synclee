# -*- coding: UTF-8 -*-
# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from synclee.work.models import Work
from synclee.billboard.models import Board

def refresh_board(request):
    new_board = Board()
    key = request.GET.get('key')
    if not key == 'synclee_forever':
        return HttpResponse("little buster")
    all_work = Work.objects.all()
    top_works = all_work.order_by('-push_today')[:20]
    top_fiction = all_work.filter(catalog__name='文字').order_by('-push_today')[:20]
    top_illust = all_work.filter(catalog__name='图集').order_by('-push_today')[:20]
    top_comic = all_work.filter(catalog__name='漫画').order_by('-push_today')[:20]
    w_list = f_list = i_list = c_list = ""
    for i in range(20):
        try:
            w_list += str(top_works[i].id) + ','
        except:
            pass
        try:
            f_list += str(top_fiction[i].id) + ','
        except:
            pass
        try:
            i_list  += str(top_illust[i].id) + ','
        except:
            pass
        try:
            c_list  += str(top_comic[i].id) + ','
        except:
            pass
    new_board.order = w_list
    new_board.order_fiction = f_list
    new_board.order_comic = c_list
    new_board.order_illust = i_list
    for u in User.objects.all():
        u.pushed.clear()
        u.save()
    for a in all_work:
        a.push_today = 0
        a.save()
    new_board.save()
    return HttpResponse('Board has been Refreshed')

def show_board(request):
    user = request.user
    type = request.GET.get('type')
    the_board = Board.objects.all().order_by('-id')[0]
    works = the_board.get_board(type)
    if type == 'fiction':
        cata = '文字'
    if type == 'illust':
        cata = '图集'
    if type == 'comic':
        cata = '漫画'
    else:
        cata = '全部'
    context = {}
    context['user'] = user
    context['works'] = works
    context['cata'] = cata
    return render_to_response('billboard/show_board.shtml', context)