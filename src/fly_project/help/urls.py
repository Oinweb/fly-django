from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
     url(r'^help$', views.help_page, name='help'),
     url(r'^help/contact$', views.help_contact, name='help_contact'),
)
