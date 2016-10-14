from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions
from api.models import Me
from api.models import XPLevel


class AttachIPAddressMiddleware(object):
    """
        Utility middleware for getting the IP. Source: http://stackoverflow.com/a/4581997
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Discover the IP address of the user and attach it to the request.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.ip_address = x_forwarded_for.split(',')[0]
        else:
            request.ip_address = request.META.get('REMOTE_ADDR')

        # Run the view.
        return self.get_response(request)


class AttachMeMiddleware(object):
    """
        The purpose of this middleware is to lookup the 'Me' object for
        the authenticated user and attach it to the request. If the user
        is authenticated and does not have a 'Me' object then it will be
        created in this middleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated():
            try:
                request.me = Me.objects.get(user=request.user)
            except Me.DoesNotExist:
                request.me = Me.objects.create(
                    user_id=request.user.id,
                    xplevel=XPLevel.objects.get_or_create_for_level_one(),
                )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # (Do Nothing...)

        return response  # Finish our middleware handler.


class AttachTokenMiddleware(object):
    """
        The purpose of this middleware is to attach a 'token' variable to
        the request if the User has been logged in and if a Token does not
        exist then create one.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated():
            try:
                request.token = Token.objects.get(user_id=request.user.id)
            except Token.DoesNotExist:
                request.token = Token.objects.create(user_id=request.user.id)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # (Do Nothing ...)

        return response  # Finish our middleware handler.


class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # (Do nothing)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # (Do nothing)

        return response

    def process_exception(self, request, exception):
        """
            The purpose of this function is to caputure the "AuthCanceled"
            exception raised by the "Python Social Auth" library and to
            redirect the user to the /en/authentication page.
        """
        if hasattr(social_exceptions, 'AuthCanceled'):
            print(exception)
            language = get_language()
            url = reverse('authentication')
            return HttpResponseRedirect(url)
        else:
            print(exception)
            raise exception
