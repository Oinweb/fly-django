from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from fly_project import settings
from api.models import Share
from api.models import Notification


def share_page(request, notification_id):
    # Fetch the Share History for the particular Notification. If there doesn't
    # exist then we need to create it.
    try:
        share = Share.objects.get(notification_id=notification_id)
    except Share.DoesNotExist:
        # Fetch the notification for the newly created share and
        # error 404 if Notification doesn't exist.
        notification = get_object_or_404(Notification, id=notification_id)

        # Handle Level Up
        if notification.type == 1:
            share = Share.objects.create(
                notification_id=notification_id,
                user_id=request.user.id,
                type=1,
                xplevel=notification.xplevel,
            )

        # Handle Badge
        elif notification.type == 2:
            share = Share.objects.create(
                notification_id=notification_id,
                user_id=request.user.id,
                type=2,
                badge=notification.badge,
            )
                
        # Custom
        else:
            share = Share.objects.create(
                notification_id=notification_id,
                user_id=request.user.id,
                type=3,
                custom_title=notification.title,
                custom_description=notification.description,
                custom_url=''
            )

        # Delete the Notification.
        notification.delete()
            
    # Pick the appropriate page for the Share.
    url = ''
    if share.type == 1:
        url = 'share/levelup.html'
    elif share.type == 2:
        url = 'share/badge.html'
    else:
        url = 'share/custom.html'

    # Render the Share.
    return render(request, url, {
        'settings': settings,
        'share': share,
    })
