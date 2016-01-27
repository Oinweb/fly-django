from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='/authentication')
def dashboard_page(request):
    return render(request, 'dashboard/view.html',{})