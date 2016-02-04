import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUser
from api.serializers import CreditGoalSerializer
from api.models import CreditGoal


class CreditGoalFilter(django_filters.FilterSet):
    class Meta:
        model = CreditGoal
        fields = ['id', 'user', 'created', 'is_locked', 'unlocks', 'is_closed', 'was_accomplished', 'earned_xp', 'points', 'times', 'period',]


class CreditGoalViewSet(viewsets.ModelViewSet):
    queryset = CreditGoal.objects.all()
    serializer_class = CreditGoalSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = CreditGoalFilter
