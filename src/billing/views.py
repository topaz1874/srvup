import random

from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages

from .models import Transaction
from .signals import become_member
# Create your views here.
def upgrade(request):

    Transaction.objects.create_newtrans(
        user=request.user,
        transaction_id='safwfaq%sasfqfw' % (random.randint(1,10000)),
        amount=25.00,
        card_type='visa',)

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


def history(request):
    histories = request.user.transaction_set.get_success()
    return render(request, 'billing/history.html', {'queryset': histories})