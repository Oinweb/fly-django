import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
#from api.permissions import IsEmployeeUser
from api.serializers import ImageUploadSerializer
from api.models import ImageUpload


class ImageUploadFilter(django_filters.FilterSet):
    class Meta:
        model = ImageUpload
        fields = ['user_id',]


class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = ImageUploadFilter
