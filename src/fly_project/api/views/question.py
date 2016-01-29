import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import QuestionSerializer
from api.models import Question


class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = ['id', 'created', 'quiz', 'num', 'title', 'description', 'type', 'a', 'a_is_correct', 'b', 'b_is_correct', 'c', 'c_is_correct', 'd', 'd_is_correct', 'e', 'e_is_correct', 'f', 'f_is_correct', 'true_choice', 'false_choice', 'answer',]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = QuestionFilter
