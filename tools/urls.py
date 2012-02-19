from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('tools',
    url(r'^upload/check_existing/$', 'upload.views.check_existing', name='check_existing'),
    url(r'^upload/upload_image/(?P<user_id>\d+)/$', 'upload.views.upload_image', name='upload_image'),
    url(r'^zip/export_work/(?P<work_id>\d+)/$', 'zip.views.export_work', name='export_work'),
    url(r'^zip/import_work/$', 'zip.views.import_work', name='import_work'),
    
    #url(r'^write_work/(?P<work_id>\d+)/$', 'write_work', name='write_work'),
)
