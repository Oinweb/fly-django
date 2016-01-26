from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    # Custom Files
    url(r'^robots\.txt$', views.robots_txt_page, name='robots'),
    url(r'^humans\.txt$', views.humans_txt_page, name='humans'),
    url(r'^$', views.land_page, name='landpage'),
                       
    # Testing that AdminEmailHandler works.
    #url(r'^500$', views.http_500_error_page), # For debugging purposes only!
)
