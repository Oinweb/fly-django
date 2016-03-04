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
    response_data = {'status': 'failure', 'message': 'There was an error sending the email'}
    print(request.language)
    if request.method == 'POST':
        print('post')
        try:
            contact_list = [settings.DEFAULT_TO_EMAIL]
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            text = "FROM: " + email + "\n"
            text += "NAME: " + name + "\n"
            text += "PHONE: " + phone + "\n"
            text += "MESSAGE: " + message + "\n"

            send_mail(
                "New Inquiry",
                text,
                settings.EMAIL_HOST_USER,
                contact_list,
                fail_silently = False
            )
            response_data = {'status': 'success', 'message': 'Thank you for contacting us!'}
        except Exception as e:
            response_data = {'status': 'failure', 'message': 'there was some kind of error'}

    return HttpResponse(json.dumps(response_data), content_type='application/json')