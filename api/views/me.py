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
from rest_framework.decorators import detail_route
from django.core.management import call_command


class MeFilter(django_filters.FilterSet):
    class Meta:
        model = Me
        fields = ['id', 'created', 'user', 'xp', 'xp_percent', 'xplevel', 'badges', 'courses', 'wants_newsletter', 'wants_goal_notify', 'wants_course_notify', 'wants_resource_notify',]


class MeViewSet(viewsets.ModelViewSet):
    queryset = Me.objects.all()
    serializer_class = MeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = MeFilter


    @detail_route(methods=['get'], permission_classes=[IsUser])
    def evaluate_me(self, request, pk=None):
        """
            Function will perform the following:
            - Iterate through all the Goals and re-compute the score
            - Add Badge(s) when the User reaches a certain XP-Level
            -
        """
        call_command('evaluate_me',str(pk))
        return Response({'status': 'success', 'message': 'successfully ran game loop for user.'})
