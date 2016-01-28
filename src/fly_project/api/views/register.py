import json
import django_filters
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from api.authentication import CsrfExemptSessionAuthentication, BasicAuthentication
from api.pagination import LargeResultsSetPagination
from api.serializers import RegisterSerializer
from api.models import BannedDomain

class RegisterViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
        A viewset for viewing and editing user instances.
    """
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
   
    @detail_route(methods=['post',])
    def registration(self, request, pk=None):
        """
            Function will fetch the login credentials and either log the user in
            or return error. To call this function, use this URL:
            --------------------------------------------
            /api/registers/0/registration/?format=json
            --------------------------------------------
        """
        # ALGORITHM: Attempt to decode the data the way iOS encoded it
        #            else we have to just attempt to decode the data raw.
        try:
            for data in request.data:
                json_arr = json.loads( data )
                serializer = RegisterSerializer(data=json_arr) # iOS Version
        except Exception as e:
            serializer = RegisterSerializer(data=request.data) # Mobile Version
        
        if serializer.is_valid():
            username = serializer.data['username'].lower()
            email = serializer.data['email']
            password = serializer.data['password']
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']
        
            # Validate to ensure the user is not using an email which is banned in
            # our system for whatever reason.
            banned_domains = BannedDomain.objects.all()
            for banned_domain in banned_domains:
                if email.count(banned_domain.name) > 0:
                    return Response({
                        'status' : 'failure',
                        'errors' : {'email':'this emal domain is not accepted by our system'}
                    })

            # Validate to ensure the email has not been taken by another user.
            try:
                user = User.objects.get(email=email)
                return Response({
                    'status': 'failed',
                    'errors': {'email':'has already been taken by another user.'}
                })
            except User.DoesNotExist:
                pass

            # Create our new user
            try:
                user = User.objects.create_user(
                    username,
                    email,
                    password,
                )
                user.first_name = serializer.data['first_name']
                user.last_name = serializer.data['last_name']
                # user.is_active = False;  # Need email verification to change status.
                user.save()

                return Response({ # Return success message.
                    'status': 'success',
                    'errors': [],
                    'user_id': user.id,
                })
            except Exception as e:
                return Response({
                    'status' : 'failure',
                    'errors' : {'Unknown':'An unknown error occured, failed registering user.'}
                })
        else:
            return Response({
                'status': 'failed',
                'errors': str(serializer.errors),
            })