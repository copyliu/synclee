from django.contrib.auth.models import User
from django.conf.urls.defaults import url

from tastypie.resources import ModelResource
from works.models import Work, TimeLine
from accounts.models import Invitation

class UserResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        queryset = User.objects.all()
        fields = ['username', 'first_name', 'last_name', 'last_login', 'id']
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[a-z-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
class WorkResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        queryset = Work.objects.all()
        
class WorkResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        queryset = Work.objects.all()
