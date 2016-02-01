from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fly_project import settings


@login_required(login_url='/authentication')
def account_page(request):
    return render(request, 'account/profile.html',{
        'settings': settings,
    })


@login_required(login_url='/authentication')
def notifications_page(request):
    return render(request, 'account/notification.html',{
        'settings': settings,
    })