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
    url(r'^control$', views.control, name='control'),
    # url(r'^detail/(?P<serie_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<serie_id>[0-9]+)/$', views.control_edit, name='control_edit'),
    url(r'^delete/(?P<serie_id>[0-9]+)/$', views.control_delete, name='control_delete'),
    
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
    
]
