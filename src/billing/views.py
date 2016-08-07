from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from .signals import become_member
# Create your views here.
def upgrade(request):
    context = {}
    next_url = request.GET.get('next')
    member = request.POST.get('member')
    month = request.POST.get('month')

    if member:
        become_member.send(sender=request.user,
                            month=str(month))
        messages.success(request, 'HoHO, now you become our site member, enjoy.')
        return HttpResponseRedirect(next_url)
    return render(request, 'billing/upgrade.html', context)

 