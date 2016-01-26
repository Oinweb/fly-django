"""fly_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.conf.urls.static import static, settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap


sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [
    # Multi-Language Support
    url(r'^i18n/', include('django.conf.urls.i18n')),
               
    # Administration Access
    url(r'^admin/', admin.site.urls),
               
    # Django REST Framework
    url(r'', include('api.urls')),
               
    # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Application URLs.
urlpatterns += i18n_patterns('',
    url(r'', include('landpage.urls')),
)