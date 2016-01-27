from django.conf.urls import url, include
from api.views import imageupload
from api.views import banned_domain
from api.views import banned_ip
from api.views import banned_word
from api.views import register
from api.views import login
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'imageuploads', imageupload.ImageUploadViewSet)
router.register(r'banned_domains', banned_domain.BannedDomainViewSet)
router.register(r'banned_ips', banned_ip.BannedIPViewSet)
router.register(r'banned_words', banned_word.BannedWordViewSet)
router.register(r'registers', register.RegisterViewSet)
router.register(r'logins', login.LoginViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Used for Token Based authentication.
from rest_framework.authtoken import views
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]