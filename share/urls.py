from django.conf.urls import include, url
from . import views


urlpatterns = (
    url(r'^share/(\d+)/$', views.share_page, name='share_page'),
)
