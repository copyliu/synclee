from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('tools',
    url(r'^upload/check_existing/$', 'upload.views.check_existing', name='check_existing'),
    url(r'^upload/upload_image/(?P<user_id>\d+)/$', 'upload.views.upload_image', name='upload_image'),
    #url(r'^write_work/(?P<work_id>\d+)/$', 'write_work', name='write_work'),
)
