from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


def robots_txt_page(request):
    return render(request, 'landpage/txt/robots.txt', {}, content_type="text/plain")


def humans_txt_page(request):
    return render(request, 'landpage/txt/humans.txt', {}, content_type="text/plain")


def land_page(request):
    return render(request, 'landpage/view.html',{
          'test':'',        
    })