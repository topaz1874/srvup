from django.conf.urls import patterns, include, url
from django.contrib import admin
# from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    #url(r'^about/$', TemplateView.as_view(template_name='base.html'), name='home'),
    #url(r'^pricing/$', TemplateView.as_view(template_name='base.html'), name='home'),
    #url(r'^contact_us/$', TemplateView.as_view(template_name='pricing.html'), name='home'),
    url(r'^$', 'srvup.views.home', name='home'),
    url(r'^staff/$','srvup.views.staff_home', name='staff'),
    url(r'^register/$','account.views.user_register', name='register'),
    url(r'^logout/$', 'account.views.auth_logout', name='logout'),
    url(r'^login/$', 'account.views.auth_login', name='login'),
    url(r'^projects/list/$',
        'video.views.category_list', name='category_list'),
    url(r'^projects/(?P<cat_slug>[-\w]+)/$',
        'video.views.category_detail', name='category_detail'),
    url(r'^projects/(?P<cat_slug>[-\w]+)/(?P<vid_slug>[-\w]+)/$',
        'video.views.video_detail', name='video_detail'),

    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) 
#auth login/logout


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
