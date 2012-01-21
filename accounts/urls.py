from django.conf.urls.defaults import patterns, url
from accounts.forms import LoginForm
from django.contrib.auth import views as auth_views

urlpatterns = patterns('accounts.views',
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form':LoginForm }, name = 'login'),
    url(r'^register/$', 'register', name = 'register'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^profile/(?P<user>\w+)/$', 'profile', name='profile'),
    url(r'^settings/(?P<item>\w+)/$', 'settings', name='settings'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'home.html'}, name='logout'),
)
