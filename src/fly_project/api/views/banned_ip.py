import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import BannedIPSerializer
from api.models import BannedIP


class BannedIPFilter(django_filters.FilterSet):
    reason = django_filters.CharFilter(name="reason", lookup_type=("icontains"))
    class Meta:
        model = BannedIP
        fields = ['address','banned_on','reason',]


class BannedIPViewSet(viewsets.ModelViewSet):
    queryset = BannedIP.objects.all()
    serializer_class = BannedIPSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = BannedIPFilter