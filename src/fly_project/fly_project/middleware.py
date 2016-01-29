from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import get_language
from django.contrib.auth.models import User
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
                    user=request.user,
                    xplevel=XPLevel.objects.get_or_create_for_level_one(),
                )
    
        return None  # Finish our middleware handler.
