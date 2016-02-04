import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUser
from api.serializers import FinalGoalSerializer
from api.models import FinalGoal


class FinalGoalFilter(django_filters.FilterSet):
    class Meta:
        model = FinalGoal
        fields = ['id', 'user', 'created', 'is_locked', 'unlocks', 'is_closed', 'was_accomplished', 'earned_xp', 'amount', 'for_want', 'for_other_want',]


class FinalGoalViewSet(viewsets.ModelViewSet):
    queryset = FinalGoal.objects.all()
    serializer_class = FinalGoalSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = FinalGoalFilter
