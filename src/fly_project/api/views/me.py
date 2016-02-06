import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUser
from api.serializers import MeSerializer
from api.models import Me


class MeFilter(django_filters.FilterSet):
    class Meta:
        model = Me
        fields = ['id', 'created', 'user', 'avatar', 'xp', 'xp_percent', 'xplevel', 'badges', 'courses', 'wants_newsletter', 'wants_goal_notify', 'wants_course_notify', 'wants_resource_notify',]


class MeViewSet(viewsets.ModelViewSet):
    queryset = Me.objects.all()
    serializer_class = MeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = MeFilter
