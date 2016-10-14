import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import BannedWordSerializer
from api.models import BannedWord


class BannedWordFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(name="text", lookup_type=("icontains"))
    reason = django_filters.CharFilter(name="reason", lookup_type=("icontains"))
    class Meta:
        model = BannedWord
        fields = ['text','banned_on','reason',]


class BannedWordViewSet(viewsets.ModelViewSet):
    queryset = BannedWord.objects.all()
    serializer_class = BannedWordSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = BannedWordFilter