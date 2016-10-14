from django.conf.urls import include, url
from . import views


urlpatterns = (
     url(r'^help$', views.help_page, name='help'),
     url(r'^help/contact$', views.help_contact, name='help_contact'),
)
