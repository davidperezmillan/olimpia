from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.portada, name='portada'),
    url(r'^control$', views.control, name='control'),
    # url(r'^detail/(?P<serie_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<serie_id>[0-9]+)/$', views.control_edit, name='control_edit'),
    url(r'^delete/(?P<serie_id>[0-9]+)/$', views.control_delete, name='control_delete'),
    
]