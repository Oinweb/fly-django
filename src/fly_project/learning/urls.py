from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^learning$', views.learning_page, name='learning'),
    url(r'^course/(\d+)/$', views.course_page, name='course'),
    url(r'^quiz/(\d+)/(\d+)/$', views.quiz_page, name='quiz'),
)
