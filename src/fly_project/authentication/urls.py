from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^authentication$', views.authentication_page, name='authentication'),
    url(r'^login$', views.login_page, name='login'),
    url(r'^register$', views.register_page, name='register'),
)
