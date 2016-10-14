import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUser
from api.serializers import QuestionSubmissionSerializer
from api.models import QuestionSubmission


class QuestionSubmissionFilter(django_filters.FilterSet):
    class Meta:
        model = QuestionSubmission
        fields = ['id', 'created', 'user', 'quiz', 'type', 'a', 'b', 'c', 'd', 'e', 'f', 'mark',]


class QuestionSubmissionViewSet(viewsets.ModelViewSet):
    queryset = QuestionSubmission.objects.all()
    serializer_class = QuestionSubmissionSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = QuestionSubmissionFilter
