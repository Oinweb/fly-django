import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import CourseSerializer
from api.models import Course


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = ['id', 'type', 'created', 'image', 'title', 'summary', 'description', 'video_url', 'duration', 'awarded_xp', 'has_prerequisites', 'prerequisites',]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = CourseFilter
