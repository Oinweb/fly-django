import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUser
from api.serializers import QuizSubmissionSerializer
from api.models import QuizSubmission
from django.core.management import call_command


class QuizSubmissionFilter(django_filters.FilterSet):
    class Meta:
        model = QuizSubmission
        fields = ['id', 'created', 'user', 'course', 'finished', 'is_finished', 'final_mark',]


class QuizSubmissionViewSet(viewsets.ModelViewSet):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = QuizSubmissionFilter


    @detail_route(methods=['get'], permission_classes=[IsUser])
    def evaluate(self, request, pk=None):
        """
            Function will iterate through all the submitted answers for this 
            particular Quiz and evaluate the Quiz. A final mark will be assigned
            to this Quiz and all the submitted answers will have a score 
            associated with it.
        """
        call_command('evaluate_quiz',str(pk))
        return Response({'status': 'success', 'message': '!discounts successfully applied'})