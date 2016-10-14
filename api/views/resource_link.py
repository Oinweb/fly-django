import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import ResourceLinkSerializer
from api.models import ResourceLink


class ResourceLinkFilter(django_filters.FilterSet):
    class Meta:
        model = ResourceLink
        fields = ['id','created','title','url','type',]


class ResourceLinkViewSet(viewsets.ModelViewSet):
    queryset = ResourceLink.objects.all()
    serializer_class = ResourceLinkSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = ResourceLinkFilter