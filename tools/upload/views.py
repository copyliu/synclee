from django.contrib.sessions.models import Session
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import os, time, random

@csrf_exempt
def check_existing(request):
    
    #print request.FILES['Filedata'].name
    
    return HttpResponse('0')

@csrf_exempt
def upload_image(request, work_id):
    file_ext = str(request.FILES['Filedata'].name).split('.')[-1]
    
    # dont use Django save_FOO_file, defined a new filename
    file_name = time.strftime('%Y%m%d%H%M%S')
    file_name = file_name + '_%d' % random.randint(0,100)
    
    upload_path = os.path.join('media', 'works')
    user_upload_folder = os.path.join(upload_path, work_id)
    
    if not os.path.exists(upload_path):
        os.mkdir(upload_path)
    
    if not os.path.exists(user_upload_folder):
        os.mkdir(user_upload_folder)
        
    file_upload = open( os.path.join(user_upload_folder, file_name+'.'+file_ext), 'w')
    file_upload.write(request.FILES['Filedata'].read())
    file_upload.close()
    return HttpResponse(file_name+'.'+file_ext)