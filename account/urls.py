from django.conf.urls import include, url
from . import views


urlpatterns = (
    url(r'^account$', views.account_page, name='account'),
    url(r'^notifications$', views.notifications_page, name='notifications'),
    url(r'^goal_history/(\d+)/$', views.goal_history_page, name='goal_history'),
    url(r'^badges$', views.badges_page, name='badges'),
)
