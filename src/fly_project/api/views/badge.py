import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import BadgeSerializer
from api.models import Badge


class BadgeFilter(django_filters.FilterSet):
    class Meta:
        model = Badge
        fields = ['id', 'created', 'type', 'image', 'level', 'title', 'description', 'has_xp_requirement', 'required_xp',]


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = BadgeFilter
