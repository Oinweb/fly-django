from django.conf.urls import include, url
from . import views


urlpatterns = (
    url(r'^learning$', views.learning_page, name='learning'),
    url(r'^course/(\d+)/$', views.course_page, name='course'),
    url(r'^quiz/(\d+)/$', views.quiz_home_page, name='quiz'),
    url(r'^quiz/(\d+)/question/(\d+)/$', views.quiz_question_page, name='question'),
    url(r'^quiz/(\d+)/question/finished$', views.quiz_final_question_page, name='final_question'),
)
