from django.conf.urls.defaults import *

urlpatterns = patterns('synclee.work.views',
    #/work/add/?work_catalog=fiction
    #/work/233/invite/toneylee/
    #/work/233/apply/
    url(r'^add/$', 'add_work', name='AddWork'),
    url(r'^invite/(?P<username>[\w-]+)/$', 'invite_member', name='InviteWorkMember'),
    url(r'^(?P<work_id>[\d-]+)/apply/$', 'apply_member', name='ApplyWorkMember'),
    url(r'^accept/$', 'accept_member', name='AcceptWorkMember'),
    url(r'^deny/$', 'deny_member', name='DenyWorkMember'),
    
    #/work/233/edit/text/?action=edit&text_id=466
    #/work/233/edit/text/?action=new
    #/work/233/edit/text/?action=del
    url(r'^(?P<work_id>[\d-]+)/edit/text/$', 'edit_text', name='EditWorkText'),
    url(r'^(?P<work_id>[\d-]+)/edit/gallery/$', 'edit_gallery', name='EditWorkGallery'),
    url(r'^(?P<work_id>[\d-]+)/edit/links/$', 'edit_links', name='EditWorkLink'),
    url(r'^(?P<work_id>[\d-]+)/edit/tab/$', 'edit_tab', name='EditWorkTab'),
    
    #/work/233/edit/text/?text_id=466
    #/work/233/edit/gallery/?gallery_id=466
    url(r'^(?P<work_id>[\d-]+)/text/$', 'show_text', name='ShowWorkText'),
    url(r'^(?P<work_id>[\d-]+)/refresh_text_section/$', 'refresh_text_section', name='ReWorkText'),
    url(r'^(?P<work_id>[\d-]+)/refresh_pre/$', 'refresh_pre', name='RePreWorkText'),
    url(r'^(?P<work_id>[\d-]+)/refresh_section/$', 'refresh_section', name='ReSecWorkText'),
    url(r'^(?P<work_id>[\d-]+)/refresh_next/$', 'refresh_next', name='ReNextWorkText'),
    url(r'^(?P<work_id>[\d-]+)/gallery/$', 'show_gallery', name='ShowWorkGallery'),
    
    #/work/233/sync/text/?text_id=466
    #/work/233/sync/gallery/?gallery_id=466
    url(r'^(?P<work_id>[\d-]+)/sync/text/$', 'sync_text', name='SyncWorkText'),
    url(r'^(?P<work_id>[\d-]+)/sync/gallery/$', 'sync_gallery', name='SyncWorkGallery'),
    
    #/work/233/text/section/?action=edit&text_id=466&section_id=699
    #/work/233/text/section/?action=new&text_id=466
    #/work/233/text/section/?action=del&text_id=466&section_id=699
    url(r'^(?P<work_id>[\d-]+)/text/section/$', 'edit_text_section', name='EditWorkTextSection'),
    url(r'^(?P<work_id>[\d-]+)/gallery/section/$', 'edit_gallery_section', name='EditWorkGallerySection'),
    
    url(r'^(?P<work_id>[\d-]+)/text_section/$', 'show_text_section', name='ShowWorkTextSection'),
    url(r'^(?P<work_id>[\d-]+)/gallery_section/$', 'show_gallery_section', name='ShowWorkGallerySection'),
    
    url(r'^(?P<work_id>[\d-]+)/del_text_section/$', 'delete_text_section', name='DeleteWorkTextSection'),
    url(r'^(?P<work_id>[\d-]+)/del_gallery_section/$', 'delete_gallery_section', name='DeleteWorkGallerySection'),
    
    #/work/233/issues/add/
    #/work/233/issues/466/
    #/work/233/issues/466/done/
    #/work/233/issues/
    url(r'^(?P<work_id>[\d-]+)/issues/add/$', 'add_issue', name='AddWorkIssue'),
    url(r'^(?P<work_id>[\d-]+)/issues/(?P<issue_id>[\d-]+)/$', 'view_issue', name='ViewWorkIssue'),
    url(r'^(?P<work_id>[\d-]+)/issues/(?P<issue_id>[\d-]+)/done/$', 'make_issue_done', name='DoneWorkIssue'),
    url(r'^(?P<work_id>[\d-]+)/issues/$', 'show_issue', name='ShowWorkIssue'),
    
    #/work/233/comment/?chapter_id=466
    #/work/233/comment/
    #/work/233/reply/
    #/work/233/reply/?chapter_id=466
    url(r'^(?P<work_id>[\d-]+)/refresh_comment/$', 'refresh_comment', name='RefreashWorkComment'),
    url(r'^(?P<work_id>[\d-]+)/reply/$', 'add_comment', name='AddWorkComment'),
    url(r'^(?P<work_id>[\d-]+)/del_reply/$', 'del_comment', name='DelWorkComment'),
    
    #/work/233/history/
	url(r'^(?P<work_id>[\d-]+)/history/refresh/$', 'refresh_history', name='ReWorkHistory'),
    url(r'^(?P<work_id>[\d-]+)/history/$', 'show_history', name='ShowWorkHistory'),
    url(r'^(?P<work_id>[\d-]+)/member/$', 'show_member', name='ShowWorkMember'),
    
    #/work/fiction/
    #/work/paiting/
    #/work/233/
    url(r'^(?P<work_id>[\d-]+)/share/$', 'share_work', name='ShareWork'),
    url(r'^(?P<work_id>[\d-]+)/edit/$', 'edit_work', name='EditWork'),
    url(r'^(?P<work_id>[\d-]+)/del/$', 'delete_work', name='DelWork'),
    url(r'^(?P<work_id>[\d-]+)/refresh_text/$', 'refresh_text', name='RefWorkText'),
    
    url(r'^(?P<work_id>[\d-]+)/refresh_info/$', 'refresh_info', name='RefWorkInfo'),
    
    url(r'^(?P<work_id>[\d-]+)/$', 'home', name='WorkHome'),
    url(r'^(?P<work_catalog>[\w-]+)/$', 'index', name='WorkIndex'),
    
    
)