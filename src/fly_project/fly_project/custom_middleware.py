from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import get_language


class PyFlyCustomMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to set a constant in the request
            object a value indicating which "API" key to use. API keys are set
            according to the language used.
        """
        # Attach language code to every request.
        request.language = get_language()
        
        # Finish our middleware handler.
        return None