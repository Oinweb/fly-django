import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import QuizSerializer
from api.models import Quiz


class QuizFilter(django_filters.FilterSet):
    class Meta:
        model = Quiz
        fields = ['id', 'created', 'course', 'title', 'description',]


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = QuizFilter
