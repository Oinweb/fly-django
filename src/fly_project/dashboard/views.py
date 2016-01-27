from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


def dashboard_page(request):
    return render(request, 'dashboard/view.html',{})