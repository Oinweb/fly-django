import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUserOrReadOnly
from api.serializers import ShareSerializer
from api.models import Share


class ShareFilter(django_filters.FilterSet):
    class Meta:
        model = Share
        fields = ['id', 'created', 'type', 'user', 'xplevel', 'badge', 'custom_title', 'custom_description', 'custom_url',]


class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUserOrReadOnly,)
    filter_class = ShareFilter
