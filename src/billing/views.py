import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponseRedirect,Http404
from django.contrib import messages

from .models import Transaction,Membership
from .signals import become_member,membership_date_update
# Create your views here.
def upgrade(request):

    if request.user.is_authenticated():
        context = {}
        next_url = request.GET.get('next')
        member = request.POST.get('member')
        month = request.POST.get('month')
        trans = request.POST.get('trans')

        if trans:
            newtrans = Transaction.objects.create_newtrans(
                user=request.user,
                transaction_id='safwfaq%sasfqfw' % (random.randint(1,10000)),
                amount=25.00,
                card_type='visa',)
            if newtrans.success:
                membership_instance, created = Membership.objects.get_or_create(
                    user=request.user)
                membership_date_update.send(
                    sender=membership_instance,
                    new_date_start=newtrans.timestamp,)
                messages.success(request, 'Thanks for you support, now you become our site member, enjoy.')
                return HttpResponseRedirect(next_url)


        if member:
            become_member.send(sender=request.user,
                                month=str(month))
            messages.success(request, 'HoHO, now you become our site member, enjoy.')
            return HttpResponseRedirect(next_url)
        return render(request, 'billing/upgrade.html', context)
    return Http404

@login_required
def history(request):
    histories = request.user.transaction_set.get_success()
    return render(request, 'billing/history.html', {'queryset': histories})