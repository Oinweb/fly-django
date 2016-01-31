import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
#from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUser
from api.serializers import GoalSerializer
from api.models import Goal


class GoalFilter(django_filters.FilterSet):
    class Meta:
        model = Goal
        fields = ['id', 'created', 'was_accomplished', 'user', 'type', 'amount', 'times', 'for_want', 'for_other_want', ]


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = GoalFilter
