import json
from django.http import HttpResponse
from django.shortcuts import render,Http404,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Notifications
# Create your views here.
@login_required
def all(request):
    objects = Notifications.objects.get_all_user(request.user)
    url_lst = []
    for note in objects:

        try:
            target_url = note.target_object.get_absolute_url()
        except:
            target_url = None

        context = {
            'sender': note.sender_object,
            'action': note.action_object,
            'target': note.target_object,
            'recipient': note.recipient,
            'verify_read': reverse("notification_read", kwargs={"pk": note.id}),
            'target_url': target_url,
            'verb': note.verb,
        }
        if note.target_object and note.action_object and target_url:
            url_lst.append(
                ("%s"%note.recipient,
                "%(sender)s %(verb)s <a href='%(verify_read)s?next=%(target_url)s'>%(target)s</a> with %(action)s" %context,
                "%s"%note.read)) 

        elif note.target_object and note.action_object and not target_url:
            url_lst.append(
                ("%s"%note.recipient,
                "%(sender)s %(verb)s %(target)s with %(action)s" %context,
                "%s"%note.read))            
        elif note.target_object and not note.action_object and not target_url:
            url_lst.append(
                ("%s"%note.recipient,
                "%(sender)s %(verb)s %(target)s" %context,
                "%s"%note.read))
        else:
            url_lst.append(
                ("%s"%note.recipient,
                "%(sender)s %(verb)s" %context,
                "%s"%note.read))
    context = {
        'objects': objects,
        'url_lst':url_lst,
    }
    return render(request, 'notification/all.html', context)

@login_required
def read(request, pk):
    try:
        next_url = request.GET.get('next', None)
        object_note = Notifications.objects.get(id=pk)
        if object_note.recipient == request.user:
            object_note.read = True
            object_note.save()
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(reverse('notification_all'))
        else:
            return Http404
    except:
        return HttpResponseRedirect(reverse('notification_all'))

@login_required
def get_ajax(request):
    if request.is_ajax():
        notes = Notifications.objects.get_recent_unread(request.user)
        note_lst  = []
        count = notes.count()
        for note in notes:
            note_lst.append(str(note))
        data = {
            'notifications': note_lst,
            'count': count,
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
















