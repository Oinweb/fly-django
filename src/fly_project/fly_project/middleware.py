from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions
from api.models import Me
from api.models import XPLevel



class PyFlyLanguageMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to set a constant in the request
            object a value indicating which "API" key to use. API keys are set
            according to the language used.
        """
        # Attach language code to every request.
        request.language = get_language()
        
        return None  # Finish our middleware handler.


class PyFlyMeMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to lookup the 'Me' object for
            the authenticated user and attach it to the request. If the user
            is authenticated and does not have a 'Me' object then it will be
            created in this middleware.
        """
        if request.user.is_authenticated():
            try:
                request.me = Me.objects.get(user=request.user)
            except Me.DoesNotExist:
                request.me = Me.objects.create(
                    user_id=request.user.id,
                    xplevel=XPLevel.objects.get_or_create_for_level_one(),
                )
    
        return None  # Finish our middleware handler.


class PyFlyTokenMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to attach a 'token' variable to
            the request if the User has been logged in and if a Token does not
            exist then create one.
        """
        if request.user.is_authenticated():
            try:
                request.token = Token.objects.get(user_id=request.user.id)
            except Token.DoesNotExist:
                request.token = Token.objects.create(user_id=request.user.id)
    
        return None  # Finish our middleware handler.

    
class PyFlySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        """
            The purpose of this function is to caputure the "AuthCanceled"
            exception raised by the "Python Social Auth" library and to 
            redirect the user to the /en/authentication page.
        """
        if hasattr(social_exceptions, 'AuthCanceled'):
            #print("Redirecting")
            print(exception)
            language = get_language()
            url = "/" + language + "/authentication"
            return HttpResponseRedirect(url)
        else:
            raise exception
