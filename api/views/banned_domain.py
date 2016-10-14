import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import BannedDomainSerializer
from api.models import BannedDomain


class BannedDomainFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    reason = django_filters.CharFilter(name="reason", lookup_type=("icontains"))
    class Meta:
        model = BannedDomain
        fields = ['name','banned_on','reason',]


class BannedDomainViewSet(viewsets.ModelViewSet):
    queryset = BannedDomain.objects.all()
    serializer_class = BannedDomainSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = BannedDomainFilter