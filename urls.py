from django.conf.urls.defaults import *
#from satchmo_store.urls import urlpatterns
from django.conf import settings
from django.contrib import admin
from djapian import load_indexes
#from overexposure.feeds import  BlogFeed


load_indexes()
admin.autodiscover()
feeds={
 #   'blogs': BlogFeed,       
}
urlpatterns = patterns('',
    # Example:
    # (r'^sjphoto/', include('sjphoto.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sjphoto.base.views.basic.home_page', name="sjphoto_homepage"),
    url(r'^gallery/(?P<slug>[-\w]+)/(?P<obj_id>\d+)/$', 'sjphoto.base.views.basic.home_page', name="sjphoto_feature_gallery_detail"),
    url(r'^gallery/upload/$', 'sjphoto.base.views.basic.gallery_upload', name="sjphoto_gallery_upload"),
    url(r'^login/$', 'sjphoto.base.views.basic.login_user', name="sjphoto_login_user"),
    url(r'^ajax/login/$', 'sjphoto.base.views.ajax.ajax_login', name="sjphoto_ajax_login_user"),
    url(r'^logout/$', 'sjphoto.base.views.basic.logout_user', name="sjphoto_logout_user"),
    url(r'^mail/multicompose/$', 'sjphoto.base.views.basic.multi_compose', name="sjphoto_multi_compose"),
    url(r'^search/users/$', 'sjphoto.base.views.basic.user_search', name="sjphoto_user_search"),
    url(r'^ajax/exif/(?P<photo_id>\d+)/$', 'sjphoto.base.views.ajax.get_exif', name="sjphoto_ajax_exif_url"),
    url(r'^upload/photo/$', 'sjphoto.base.views.ajax.photo_upload', name="sjphoto_photo_test"),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="overexposure_blog_feed"),
    url(r'^search/photos/$', 'sjphoto.base.views.search.photo_search', name="sjphoto_photo_search"),
    url(r'^search/$', 'sjphoto.base.views.search.ajax_main_search', name='sjphoto_main_search'),
    
)

urlpatterns += patterns('',
   # url(r'^clients/', include('sjphoto.clientmanager.urls')),
     (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT,'show_indexes': True}),                        
)
urlpatterns += patterns('sjphoto.base.views.basic',
   url(r'^gallery/(?P<slug>[-\w]+)/$', 'gallery_view', name='pl-gallery'),                        
)
urlpatterns += patterns('',
  #  url(r'^blog/', include('overexposure.urls')),
)
urlpatterns += patterns('',
    url(r'^mail/', include('messages.urls')),
)
urlpatterns += patterns('',
#    url(r'^albums/', include('photologue.urls')),
)
urlpatterns += patterns('',
    url(r'^users/', include('registration.urls')),                        
)
urlpatterns += patterns('sjphoto.base.views.contests',
   url(r'^contest/(?P<slug>[-\w]+)/(?P<ct_id>\d+)-(?P<obj_id>\d+)/$', 'photo_contest_detail', name='sjphoto_contest_detail'),                        
)
urlpatterns += patterns('',
    url(r'^comments/', include('django.contrib.comments.urls')),
)
urlpatterns += patterns('',
    url(r'^contact/', include('contact_form.urls')),
)
urlpatterns += patterns('sjphoto.base.views.gallery',
    url(r'^albums/$', 'gallery_list', name='sjphoto_gallery_list'),
    url(r'albums/(?P<slug>[-\w]+)/(?P<obj_id>\d+)/$', 'gallery_detail', name="sjphoto_gallery_detail"),
)
urlpatterns += patterns('',
    url(r'likes/', include('likeables.urls'))                        
)
urlpatterns += patterns('',
#   url(r'^generic_photo/', include('photologue.urls')),
)
