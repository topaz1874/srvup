from django.shortcuts import render

from .models import Notifications
# Create your views here.
def all(request):
    objects = Notifications.objects.all()
    unread = Notifications.objects.get_unread(request.user)
    context = {
        'objects': objects,
        'unread': unread,
    }
    return render(request, 'notification/all.html', context)