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
    # url(r'^visto/(?P<visto_id>[0-9]+)/$', views.visto_ajax, name='visto'),
    url(r'^ficha/(?P<ficha_id>[0-9]+)/$', views.ver_ficha, name='ver_ficha'),
    

]
