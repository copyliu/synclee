from django.conf.urls.defaults import patterns, url
from accounts.forms import LoginForm
from django.contrib.auth import views as auth_views

urlpatterns = patterns('accounts.views',
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form':LoginForm }, name = 'login'),
    url(r'^register/$', 'register', name = 'register'),
    url(r'^profile/(?P<username>\w+)/$', 'profile', name='profile'),
    url(r'^notice/$', 'notice', name = 'notice'),
    url(r'^settings/(?P<item>\w+)/$', 'settings', name='settings'),
    url(r'^reset/$', 'reset_psw', name='reset_psw'),
    url(r'^reset/confirm/(?P<tmp_psw>\w+)/$', 'reset_psw_confirm', name = 'reset_psw_confirm'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'home.html'}, name='logout'),
    url(r'^users/$', 'list_user', name='users'),
)