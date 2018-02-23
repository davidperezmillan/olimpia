from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    

    url(r'^$', views.list, name='index'),
    url(r'^index', views.index, name='index'),
    
    
    url(r'^list', views.list, name='list'),
    
    
    url(r'^visto/(?P<visto_id>[0-9]+)/$', views.visto, name='visto'),
    url(r'^visto_all/(?P<ficha_id>[0-9]+)/$', views.visto_all, name='visto_all'),
    url(r'^visto_all_session/(?P<ficha_id>[0-9]+)/(?P<session_id>[0-9]+)/$', views.visto_all_session, name='visto_all_session'),
    
    url(r'^ficha/(?P<ficha_id>[0-9]+)/$', views.ver_ficha, name='ver_ficha'),
    
    url(r'^info/(?P<ficha_id>[0-9]+)/$', views.info_ficha, name='info_ficha'),
    
    url(r'^upload_file', views.upload_file, name='upload_file'),
    # url(r'^resultado', views.resultado, name='resultado'), # Creo que a esta no podemos ir directamente
    

]
