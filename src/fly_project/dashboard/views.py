from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from fly_project import settings
from api.models import Badge, Me, Notification


@login_required(login_url='/authentication')
def dashboard_page(request):
    # BADGE ID #1
    # Check to see if the logged in User has the Badge wit the ID #1. If not
    # then create it now.
    me = get_object_or_404(Me, user=request.user.id)
    badge = get_object_or_404(Badge, id=1)
    if badge not in me.badges.all():
        me.badges.add(badge)
        Notification.objects.create(
            type=2,
            title=badge.title,
            description=badge.description,
            user=me.user,
            badge=badge,
        )

    return render(request, 'dashboard/view.html',{
        'settings': settings,
    })