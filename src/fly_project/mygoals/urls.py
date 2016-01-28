from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
     url(r'^mygoals$', views.mygoals_page, name='my_goals'),                  
)
