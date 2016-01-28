import django_filters
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import _get_new_csrf_key as get_new_csrf_key
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import detail_route, list_route
from api.authentication import CsrfExemptSessionAuthentication, BasicAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import LoginSerializer
from rest_framework import permissions


class UserBelongsToUser(permissions.BasePermission):
    """
        Custom permission per user.
    """
    message = 'This object does not belong to your user account and you are not an administrator.'
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous():
            return False
        
        try:
            # Fetch the User in our system.
            user = User.objects.get(id=request.user.id)
            
            # Super Users always get access.
            if user.is_superuser:
                return True
            
            # Detect if User is owner of this object.
            return obj.id == request.user.id
        except User.DoesNotExist:
            return False


class LoginViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
        A viewset for viewing and editing user instances.
    """
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = (UserBelongsToUser,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @detail_route(methods=['post',])
    def sign_in(self, request, pk=None):
        """
            Function will fetch the login credentials and either log the user in
            or return error. To call this function, use this URL:
            --------------------------------------------
            /api/logins/0/sign_in/?format=json
            --------------------------------------------
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username'].lower()
            password = serializer.data['password']
            
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'status': 'failed', 'message': 'username not found'})
        
            # Check to see if our username and password authenticate with our system.
            user = authenticate(
                username=username,
                password=password
            )
            
            # Generate the return message according to whether we are logged in or not.
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response_data = {
                        'status': 'success',
                        'message': 'logged in',
                        'user_id': user.id,
                    #'csrf_token': get_new_csrf_key(),
                    }
                else:
                    response_data = {'status' : 'failure', 'message' : 'you are suspended'}
            else:
                response_data = {'status' : 'failure', 'message' : 'wrong username or password'}

            return Response(response_data)
        else:
            return Response({'status': 'failed', 'message': 'username and/or password are blank'})


    @detail_route(methods=['post',])
    def sign_off(self, request, pk=None):
        """
            --------------------------------------------
            /api/logins/0/sign_off/?format=json
            --------------------------------------------
        """
        logout(request)
        return Response({'status': 'sucess', 'message': 'user logged off.'})
