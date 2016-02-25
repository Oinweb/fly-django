from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from fly_project import settings
from api.models import Share


def share_page(request, share_id):
    #TODO: Implement fetching share object.
    return render(request, 'share/badge.html',{
        'settings': settings,
    })