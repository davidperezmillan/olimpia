from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    
    
    url(r'^$', views.index, name='portada'),
    url(r'^index', views.index, name='index'),
    
    
    url(r'^export$', views.export, name='export'),
    
    url(r'^visto/(?P<visto_id>[0-9]+)/$', views.visto, name='visto'),
    url(r'^visto_all/(?P<ficha_id>[0-9]+)/$', views.visto_all, name='visto_all'),
    url(r'^visto_all_session/(?P<ficha_id>[0-9]+)/(?P<session_id>[0-9]+)/$', views.visto_all_session, name='visto_all_session'),
    url(r'^ajax/visto_ajax/$', views.visto_ajax, name='visto_ajax'),
    
    
    # url(r'^articles/2003/$', views.special_case_2003),
    # url(r'^articles/([0-9]{4})/$', views.year_archive),
    # url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    # url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
    
    # url(r'^visto/(?P<visto_id>[0-9]+)/$', views.visto_ajax, name='visto'),
    url(r'^ficha/(?P<ficha_id>[0-9]+)/$', views.ver_ficha, name='ver_ficha'),
    url(r'^info/(?P<ficha_id>[0-9]+)/$', views.info_ficha, name='info_ficha'),
    url(r'^info_session/(?P<ficha_id>[0-9]+)/(?P<session_id>[0-9]+)/$', views.info_ficha_session, name='info_ficha_session'),
    

]
