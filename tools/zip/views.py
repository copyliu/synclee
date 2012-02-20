# -*- coding: utf-8 -*-
from cStringIO import StringIO
from works.models import Work, Element
from django.http import HttpResponseRedirect, HttpResponse
import os, zipfile, settings, json


def export_work(request, work_id):
    file = StringIO()
    zf = zipfile.ZipFile(file, mode='w', compression=zipfile.ZIP_DEFLATED)
    input_dir = os.path.join(settings.MEDIA_ROOT, 'cover')
    for root, dirs, files in os.walk(os.path.join(settings.MEDIA_ROOT, 'cover')):
        for f in files:
            abs_path = os.path.join(os.path.join(root, f))
            rel_path = os.path.relpath(abs_path, os.path.dirname(input_dir))
            zf.write(abs_path, rel_path, zipfile.ZIP_STORED)
    
    
    work = Work.objects.get(pk=work_id)
    elements = Element.objects.filter(work=work)
    
    export_command = []
    for element in elements:
        if element.category == 'image':
            #file = open(os.path.join(settings.MEDIA_ROOT, element.content))
            #zf.write(os.path.join(settings.MEDIA_ROOT, element.content))
            #zf.write(settings.MEDIA_ROOT, element.content, zipfile.ZIP_STORED)
            export_command.append({"image": element.content})
        else:
            export_command.append({"text": element.content})
    
    txt = open('temp.txt','w+')
    txt.write(str(export_command))
    txt.close()
    zf.write('temp.txt')
    
    txt = open('info.txt','w+')
    # TODO: 图片转换 "cover": work.cover,
    info = {"name": work.name, "category": work.category, "isprivate": work.isprivate, "intro": work.intro}
    txt.write(str(info))
    txt.close()
    zf.write('info.txt')
    
    zf.close()
    response = HttpResponse(file.getvalue(), mimetype="application/zip")
    response['Content-Disposition'] = 'filename=all_things.zip'
    return response


def import_work(request):
    work_zip = zipfile.ZipFile(request.FILES.get('work_zip'))
    for f in work_zip.namelist():
        work_zip.extract(f, os.path.join(settings.MEDIA_ROOT, 'bak'))
    
    info = eval(open(os.path.join(os.path.join(settings.MEDIA_ROOT, 'bak'), 'info.txt')).read())
    Work.objects.create(name=info['name'], author=request.user)
    
    temp = eval(open(os.path.join(os.path.join(settings.MEDIA_ROOT, 'bak'), 'temp.txt')).read())
    for t in temp:
        if t.keys()[0] == "text":
            print t.values()