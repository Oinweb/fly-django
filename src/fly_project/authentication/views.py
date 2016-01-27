from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


def authentication_page(request):
    return render(request, 'authentication/view.html',{})


def login_page(request):
    return render(request, 'authentication/login.html',{})


def register_page(request):
    return render(request, 'authentication/register.html',{})