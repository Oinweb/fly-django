from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^learning$', views.learning_page, name='learning'),                  
)
