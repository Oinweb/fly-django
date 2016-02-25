from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^share/(\d+)/$', views.share_page, name='share_page'),
)
