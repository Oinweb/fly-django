from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^$', views.land_page, name='landpage'),
    url(r'^contact$', views.contact, name='contact'),
)
