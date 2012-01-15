from django.conf.urls.defaults import *

urlpatterns = patterns('synclee.club.views',
    #/club/add/
    #/club/windancer/invite/toneylee/
    #/club/windancer/apply/
    url(r'^add/$', 'add_club', name='AddClub'),
    url(r'^(?P<club_name>[\w-]+)/invite/(?P<username>[\w-]+)/$', 'invite_member', name='InviteClubMember'),
    url(r'^(?P<club_name>[\w-]+)/apply/$', 'apply_member', name='ApplyClubMember'),
    url(r'^(?P<club_name>[\w-]+)/accept/$', 'accept_member', name='AcceptClubMember'),
    
    #/club/windancer/edit/text/?action=edit&text_id=466
    #/club/windancer/edit/text/?action=new
    #/club/windancer/edit/text/?action=del
    url(r'^(?P<club_name>[\w-]+)/edit/text/$', 'edit_text', name='EditClubText'),
    url(r'^(?P<club_name>[\w-]+)/edit/gallery/$', 'edit_gallery', name='EditClubGallery'),
    #url(r'^(?P<club_name>[\w-]+)/edit/$', 'edit_club', name='EditClub'),
    
    #/club/windancer/edit/text/?text_id=466
    #/club/windancer/edit/gallery/?gallery_id=466
    url(r'^(?P<club_name>[\w-]+)/text/$', 'show_text', name='ShowClubText'),
    url(r'^(?P<club_name>[\w-]+)/gallery/$', 'show_gallery', name='ShowClubGallery'),
    
    #/club/windancer/text/section/?action=edit&text_id=466&section_id=699
    #/club/windancer/text/section/?action=new&text_id=466
    #/club/windancer/text/section/?action=del&text_id=466&section_id=699
    url(r'^(?P<club_name>[\w-]+)/text/section/$', 'edit_text_section', name='EditClubTextSection'),
    url(r'^(?P<club_name>[\w-]+)/gallery/section/$', 'edit_gallery_section', name='EditClubGallerySection'),
    
    #/club/windancer/

    url(r'^(?P<club_name>[\w-]+)/$', 'home', name='ClubHome'),
    
    #/club/windancer/233/
    #/club/windancer/project/add/
    #/club/windancer/233/gallery/
    url(r'^(?P<club_name>[\w-]+)/(?P<project_id>[\d-]+)/$', 'project_home', name='ProjectHome'),
    url(r'^(?P<club_name>[\w-]+)/project/add/$', 'add_project', name='AddProject'),
    url(r'^(?P<club_name>[\w-]+)/(?P<project_id>[\d-]+)/gallery/$', 'show_project_gallery', name='ShowProjectGallery'),
    
    #/club/windancer/233/edit/work/
    #/club/windancer/233/edit/gallery/?gallery_id=466
    #/club/windancer/233/edit/
    url(r'^(?P<club_name>[\w-]+)/(?P<project_id>[\d-]+)/edit/work/$', 'edit_project_work', name='EditProjectWork'),
    url(r'^(?P<club_name>[\w-]+)/(?P<project_id>[\d-]+)/edit/gallery/$', 'edit_project_gallery', name='EditProjectGallery'),
    #url(r'^(?P<club_name>[\w-]+)/(?P<project_id>[\d-]+)/edit/$', 'edit_project', name='EditProject'),
    url(r'^', 'index', name='ClubIndex'),
)