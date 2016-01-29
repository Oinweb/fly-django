import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import QuizSerializer
from api.models import Quiz


class QuizFilter(django_filters.FilterSet):
    class Meta:
        model = Quiz
        fields = ['id', 'created', 'quiz', 'num', 'title', 'description', 'type', 'a', 'a_is_correct', 'b', 'b_is_correct', 'c', 'c_is_correct', 'd', 'd_is_correct', 'e', 'e_is_correct', 'f', 'f_is_correct', 'true_choice', 'false_choice', 'answer',]


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = QuizFilter
