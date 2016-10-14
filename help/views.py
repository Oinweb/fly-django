import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fly_project import settings
from django.core.mail import send_mail


@login_required(login_url='/authentication')
def help_page(request):
    return render(request, 'help/view.html',{
        'settings': settings,
    })

@login_required(login_url='/authentication')
def help_contact(request):
    response_data = {'status': 'failure', 'message': 'There was an error sending the email', 'sent_status': 'unsent'}
    print(request.method)
    if request.method == 'POST':
        try:
            contact_list = [settings.DEFAULT_TO_EMAIL]
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            text =  "SENT FROM: FLY App Help\n"
            text += "FROM:    " + email + "\n"
            text += "NAME:    " + name + "\n"
            text += "SUBJECT: " + subject + "\n\n"
            text += message + "\n"

            send_mail(
                "New Inquiry",
                text,
                settings.EMAIL_HOST_USER,
                contact_list,
                fail_silently = False
            )
            response_data = {'status': 'success', 'message': 'Thank you for contacting us!', 'sent_status': 'sent'}
        except Exception as e:
            response_data = {'status': 'failure', 'message': str(e), 'sent_status': 'error'}



    return render(request, 'help/view.html', {'response': response_data})