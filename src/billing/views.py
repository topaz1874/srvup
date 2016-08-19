from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render,HttpResponseRedirect,Http404

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
        # generate client token 
        client_token = braintree.ClientToken.generate()
        context = {'client_token':client_token}

        next_url = request.GET.get('next')
        member = request.POST.get('member')
        month = request.POST.get('month')
        merchant_customer_id = None

        try:
            merchant_obj = UserMerchantID.objects.get(user=request.user)
        except UserMerchantID.DoesNotExist:
            #create a new braintree customer
            new_customer_result = braintree.Customer.create({})
            #customer successed record customer id to UserMerchantID table
            if new_customer_result.is_success:
                merchant_customer_id = new_customer_result.customer.id
                merchant_obj, created = UserMerchantID.objects.get_or_create(
                    user=request.user,
                    customer_id=merchant_customer_id)
                print """Customer created with id = {0}""".format(new_customer_result.customer.id)
            else:
                print """Error: {0}""".format(new_customer_result.message)
        except:
            pass
        # clicked pay button the request post  would send payment method nonce
        # update customer payment method
        # receive payment method token aka credit card token
        merchant_customer_id = merchant_obj.customer_id
        nonce = request.POST.get('payment_method_nonce', None)
        if nonce is not None:
            update_customer_result = braintree.Customer.update(merchant_customer_id,{
                'payment_method_nonce':nonce,
                })
            credit_card_token = update_customer_result.customer.credit_cards[0].token

            #create a new braintree subscription with token
            subscription_result = braintree.Subscription.create({
                "payment_method_token": credit_card_token,
                "plan_id":PLAN_ID,
                })
            # subscription success record subscription id to Transaction table
            if subscription_result.is_success:
                print "success" 
                trans_id = subscription_result.subscription.id 
                #need to amend  transaction id  there were suscription id for now  
                #in Trans table order id was composed by trans id 
                newtrans = Transaction.objects.create_newtrans(
                user=request.user,
                transaction_id=trans_id,
                amount=25.00,
                card_type='visa',)
            # transaction successed update membership state
            if newtrans.success:
                membership_instance, created = Membership.objects.get_or_create(
                    user=request.user)
                membership_date_update.send(
                    sender=membership_instance,
                    new_date_start=newtrans.timestamp,)
                messages.success(request, 'Thanks for you support, now you become our site member, enjoy.')
                return HttpResponseRedirect(reverse('history'))
            else:
                print "failed"




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