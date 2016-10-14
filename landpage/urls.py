from django.conf.urls import include, url
from . import views


urlpatterns = (
    url(r'^$', views.land_page, name='landpage'),
    url(r'^contact$', views.contact, name='contact'),
)
