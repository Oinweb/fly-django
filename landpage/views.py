from django.shortcuts import render
from django.http import HttpResponse
from fly_project import settings
from django.core.mail import send_mail
import json

def land_page(request):
    return render(request, 'landpage/view.html',{
        'settings': settings,
    })

def contact(request):
    response_data = {'status': 'failure', 'message': 'There was an error sending the email', 'sent_status': 'unsent'}
    print(request.method)
    if request.method == 'POST':
        try:
            contact_list = [settings.DEFAULT_TO_EMAIL]
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            text = "SENT FROM: FlyApp Landing Page\n"
            text += "     FROM: " + email + "\n"
            text += "     NAME: " + name + "\n"
            text += "    PHONE: " + phone + "\n\n"
            text += message + "\n"

            send_mail(
                "New Inquiry",
                text,
                settings.DEFAULT_FROM_EMAIL,
                contact_list,
                fail_silently = False
            )
            response_data = {'status': 'success', 'message': 'Thank you for contacting us!', 'sent_status': 'sent'}
        except Exception as e:
            response_data = {'status': 'failure', 'message': str(e), 'sent_status': 'error'}

    return render(request, 'landpage/view.html', { 'response': response_data })