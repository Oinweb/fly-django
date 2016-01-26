from django.conf.urls import url, include
#from api.views import imagebinaryupload
#from api.views import comic
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
#router.register(r'imagebinaryuploads', imagebinaryupload.ImageBinaryUploadViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^', include(router.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    url(r'^api/login/', include('rest_social_auth.urls_token')),
]

# Used for Token Based authentication.
from rest_framework.authtoken import views
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]