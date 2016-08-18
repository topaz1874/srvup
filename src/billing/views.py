import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponseRedirect,Http404
from django.contrib import messages

import braintree

from .models import Transaction,Membership,UserMerchantID
from .signals import become_member,membership_date_update
# Create your views here.

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    'q3m29r7tg2hj3fx3',
    'n7frpfxd8453gtn2',
    '15f9f94d97f31151598663137e05cfe1'
)
PLAN_ID = "monthly_plan"

def upgrade(request):

    if request.user.is_authenticated():
        context = {}
        next_url = request.GET.get('next')
        member = request.POST.get('member')
        month = request.POST.get('month')
        trans = request.POST.get('trans')

        try:
            UserMerchantID.objects.get(user=request.user)
        except UserMerchantID.DoesNotExist:
            new_customer_result = braintree.Customer.create({})
            if new_customer_result.is_success:
                UserMerchantID.objects.create(
                    user=request.user,
                    customer_id=new_customer_result.customer.id)
                print """Customer created with id = {0}""".format(new_customer_result.customer.id)
            else:
                print """Error: {0}""".format(new_customer_result.message)
        except:
            pass

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