from django.conf.urls.defaults import *

urlpatterns = patterns('synclee.profiles.views',
    url(r'^profiles/$', 'show_profile', name='ShowProfile'),
    url(r'^profiles/avatar/$', 'edit_avatar', name='EditAvatar'),
    url(r'^profiles/ability/$', 'edit_ability', name='EditAbility'),
    url(r'^(?P<username>[\w-]+)/watch/$', 'watch_work', name='Watch'),
    url(r'^(?P<username>[\w-]+)/in/$', 'joint_work', name='Joint'),
	url(r'^(?P<username>[\w-]+)/refresh/$', 're_work', name='ReWork'),
    url(r'^(?P<username>[\w-]+)/$', 'people', name='People'),
    url(r'^$', 'home', name='Home'),
)