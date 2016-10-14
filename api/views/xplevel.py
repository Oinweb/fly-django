import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import XPLevelSerializer
from api.models import XPLevel


class XPLevelFilter(django_filters.FilterSet):
    class Meta:
        model = XPLevel
        fields = ['id', 'created', 'title', 'num', 'min_xp', 'max_xp',]


class XPLevelViewSet(viewsets.ModelViewSet):
    queryset = XPLevel.objects.all()
    serializer_class = XPLevelSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = XPLevelFilter
