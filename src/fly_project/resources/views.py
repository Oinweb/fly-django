from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fly_project import settings
from fly_project import constants
from api.models import ResourceLink


@login_required(login_url='/authentication')
def resources_page(request):
    return render(request, 'resources/view.html',{
        'settings': settings,
        'constants': constants,
        'resources': ResourceLink.objects.all(),
    })