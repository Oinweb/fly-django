from django.shortcuts import render
from django.http import HttpResponse
from fly_project import settings


def authentication_page(request):
    return render(request, 'authentication/view.html',{
        'settings': settings,
    })


def login_page(request):
    return render(request, 'authentication/login.html',{
        'settings': settings,
    })


def register_page(request):
    return render(request, 'authentication/register.html',{
        'settings': settings,
    })