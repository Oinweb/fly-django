import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsUser
from api.serializers import EnrolledCourseSerializer
from api.models import EnrolledCourse


class EnrolledCourseFilter(django_filters.FilterSet):
    class Meta:
        model = EnrolledCourse
        fields = ['id', 'created', 'user', 'course', 'finished', 'is_finished', 'final_mark',]


class EnrolledCourseViewSet(viewsets.ModelViewSet):
    queryset = EnrolledCourse.objects.all()
    serializer_class = EnrolledCourseSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsUser,)
    filter_class = EnrolledCourseFilter
