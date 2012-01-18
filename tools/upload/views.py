from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import os

@csrf_exempt
def check_existing(request):
    
    #print request.FILES['Filedata'].name
    
    return HttpResponse('0')

@csrf_exempt
def upload_image(request):
    file_name = str(request.FILES['Filedata'].name);
    file_path = 'static/'
    try:
        open(file_path+file_name, 'w')
    except:
        os.mkdir(file_path)
        file_upload = open(file_path+file_name, 'w')
    else:
        file_upload = open(file_path+file_name, 'w')
    file_upload.write(request.FILES['Filedata'].read())
    file_upload.close()
    return HttpResponse('0')