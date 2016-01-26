from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


def land_page(request):
    return render(request, 'landpage/landpage.html',{})


def login_page(request):
    return render(request, 'landpage/login.html',{})


def register_page(request):
    return render(request, 'landpage/register.html',{})