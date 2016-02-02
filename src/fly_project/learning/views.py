from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fly_project import settings
from api.models import Course


@login_required(login_url='/authentication')
def learning_page(request):
    
    try:
        courses = Course.objects.all()
    except Course.DoesNotExist:
        courses = None

    return render(request, 'learning/master/view.html',{
        'settings': settings,
        'courses': courses,
    })