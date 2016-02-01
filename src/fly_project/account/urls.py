from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
     url(r'^account$', views.account_page, name='account'),
     url(r'^notifications$', views.notifications_page, name='notifications'),
                       
)
