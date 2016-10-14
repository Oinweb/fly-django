from django.conf.urls import include, url
from . import views


urlpatterns = (
    url(r'^authentication$', views.authentication_page, name='authentication'),
    url(r'^login$', views.login_page, name='login'),
    url(r'^register$', views.register_page, name='register'),
)
