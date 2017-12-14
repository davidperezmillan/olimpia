from django.conf.urls import include, url
from django.contrib import admin
from . import views
from .viewsets import SeriesViewSet
from rest_framework.routers import DefaultRouter
admin.autodiscover()


router = DefaultRouter()
router.register(r'series', SeriesViewSet)

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.portada, name='portada'),
    
    # // series
    url(r'^list$', views.list, name='list'),
    url(r'^control$', views.control, name='control'),
    url(r'^edit/(?P<serie_id>[0-9]+)/$', views.control_edit, name='control_edit'),
    url(r'^delete/(?P<serie_id>[0-9]+)/$', views.control_delete, name='control_delete'),
    
    # // torrentservers
    url(r'^listtorrentservers$', views.listtorrentservers, name='listtorrentservers'),
    url(r'^controltorrentserver$', views.control_torrentservers, name='control_torrentservers'),
    url(r'^edittorrentserver/(?P<torrentserver_id>[0-9]+)/$', views.control_edittorrent, name='control_edittorrentserver'),
    url(r'^deletetorrentserver/(?P<torrentserver_id>[0-9]+)/$', views.control_deletetorrent, name='control_deletetorrentserver'),
    
    
    # // at
    url(r'^launch/(?P<serie_id>[0-9]+)/$', views.launch_unique, name='launch_unique'),
    url(r'^launch/all/$', views.launch_all, name='launch_all'),
    url(r'^launch', views.launch_extreme, name='launch_extreme'),
    
    
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
    
]
