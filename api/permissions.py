from django.contrib.auth.models import User, AnonymousUser
from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    message = 'Only administrators are allowed to write data.'
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else: # Check permissions for write request
            if request.user.is_anonymous():
                return False
            else:
                return request.user.is_superuser


class IsUserOrReadOnly(permissions.BasePermission):
    """
        Object-level permission to only allow owners of an object to edit it.
        Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class IsUser(permissions.BasePermission):
    """
        Object-level permission to only allow owners of an object to edit and
        view it. Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous():
            return False
        else:
            # Instance must have an attribute named `owner`.
            return obj.user == request.user


#class AnonymousWriteAndIsEmployeeRead(permissions.BasePermission):
#    """
#        Custom permission to deny all non-employees from reading actions and 
#        allow all write-only actions for anonymous users.
#    """
#    message = 'Only anonymous users are able to write and authenticated users are allowed to read.'
#    def has_permission(self, request, view):
#        if request.user.is_anonymous():
#            # Check permissions for read-only request
#            if request.method in permissions.SAFE_METHODS:
#                # Note: Non-authenticated users are forbidden from reading.
#                return False
#            else:
#                return True
#        
#        # Find employee object for the user
#        try:
#            Employee.objects.get(user__id=request.user.id)
#            return True
#        except Employee.DoesNotExist:
#            return False
