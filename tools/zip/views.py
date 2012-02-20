# -*- coding: utf-8 -*-

from django.db.transaction import commit_on_success
from django.http import HttpResponseRedirect, HttpResponse
import os, zipfile, settings, json
from cStringIO import StringIO
from works.models import Work, Element

def export_work(request, work_id):
    file = StringIO()
    zf = zipfile.ZipFile(file, mode='w', compression=zipfile.ZIP_DEFLATED)
    input_dir = os.path.join(os.path.join(settings.MEDIA_ROOT, 'works'), work_id)
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            abs_path = os.path.join(os.path.join(root, f))
            rel_path = os.path.relpath(abs_path, os.path.dirname(input_dir))
            zf.write(abs_path, rel_path, zipfile.ZIP_STORED)
    
    
    work = Work.objects.get(pk=work_id)
    elements = Element.objects.filter(work=work)
    
    export_command = []
    for element in elements:
        #if element.category == 'image':
            #file = open(os.path.join(settings.MEDIA_ROOT, element.content))
            #zf.write(os.path.join(settings.MEDIA_ROOT, element.content))
            #zf.write(settings.MEDIA_ROOT, element.content, zipfile.ZIP_STORED)
            #export_command.append({"title": element.title, "image": element.content})
        #else:
        export_command.append({"category": element.category, "title": element.title, "content": element.content})
    
    txt = open('elements.txt','w+')
    txt.write(str(export_command))
    txt.close()
    zf.write('elements.txt')
    
    txt = open('info.txt','w+')
    # TODO: 图片转换 "cover": work.cover,
    info = {"id": work.id, "name": work.name, "category": work.category, "isprivate": work.isprivate, "intro": work.intro}
    txt.write(str(info))
    txt.close()
    zf.write('info.txt')
    
    zf.close()
    response = HttpResponse(file.getvalue(), mimetype="application/zip")
    response['Content-Disposition'] = 'filename=%swork%s.zip'% (request.user.username, work.id)
    return response

@commit_on_success
def import_work(request):
    work_zip = zipfile.ZipFile(request.FILES.get('work_zip'))
    temp_folder = os.path.join(settings.MEDIA_ROOT, 'temp')
    for f in work_zip.namelist():
        work_zip.extract(f, temp_folder)
    
    info = eval(open(os.path.join(temp_folder, 'info.txt')).read())
    elements = eval(open(os.path.join(temp_folder, 'elements.txt')).read())
    
    work = Work.objects.create(name=info['name'], author_id=request.user.id)
    works_folder = os.path.join(settings.MEDIA_ROOT, 'works')
    os.renames( os.path.join(temp_folder, str(info['id'])), os.path.join(works_folder, str(work.id)))
    
    for e in elements:
        args = []
        for k in e.keys():
            args.append(k+ '="'+ e[k]+ '"')
        args =  ",".join(args)
        if e['category'] == 'image':
            Element.objects.create(title=e['title'], content=e['content'].replace('works/%s'%info['id'], 'works/%s'%work.id), category=e['category'], work_id=work.id)
        else:
            Element.objects.create(title=e['title'], content=e['content'], category=e['category'], work_id=work.id)
    return HttpResponseRedirect('/works/show_work/%s' %(work.id))