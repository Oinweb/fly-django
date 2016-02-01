from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
     url(r'^help$', views.help_page, name='help'),
                       
)
