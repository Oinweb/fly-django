from django.conf.urls import include, url
from . import views


urlpatterns = (
    # Custom Files
    url(r'^robots\.txt$', views.robots_txt_page, name='robots'),
    url(r'^humans\.txt$', views.humans_txt_page, name='humans'),
    url(r'^38657648AF65578D3AD846C1DB9497C8\.txt$', views.ssl_txt_page, name='ssl'),

    # Testing that AdminEmailHandler works.
    #url(r'^500$', views.http_500_error_page), # For debugging purposes only!
)
