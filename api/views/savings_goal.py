import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUser
from api.serializers import SavingsGoalSerializer
from api.models import SavingsGoal


class SavingsGoalFilter(django_filters.FilterSet):
    class Meta:
        model = SavingsGoal
        fields = ['id', 'user', 'created', 'is_locked', 'unlocks', 'is_closed', 'was_accomplished', 'earned_xp', 'amount', 'times', 'period',]


class SavingsGoalViewSet(viewsets.ModelViewSet):
    queryset = SavingsGoal.objects.all()
    serializer_class = SavingsGoalSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = SavingsGoalFilter
