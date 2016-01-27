from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


def land_page(request):
    return render(request, 'landpage/view.html',{})