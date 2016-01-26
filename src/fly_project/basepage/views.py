from django.shortcuts import render


def robots_txt_page(request):
    return render(request, 'basepage/robots.txt', {}, content_type="text/plain")


def humans_txt_page(request):
    return render(request, 'basepage/humans.txt', {}, content_type="text/plain")

