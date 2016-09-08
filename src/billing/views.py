from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render,HttpResponseRedirect,Http404,redirect

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
                messages.error(request, "There was an error with your account. Please contact us.")
        except:
            messages.error(request, "There wan an error with the server. Please try again or contact us if problem persist.")
            pass
        # clicked pay button the request post  would send payment method nonce
        # update customer payment method
        # receive payment method token aka credit card token
        merchant_customer_id = merchant_obj.customer_id
        nonce = request.POST.get('payment_method_nonce', None)
        if nonce is not None:

            payment_method_result = braintree.PaymentMethod.create({
                "customer_id": merchant_customer_id,
                "payment_method_nonce": nonce,
                "options": {
                    "make_default": True }
                })
            the_token = payment_method_result.payment_method.token

            subscription_result = braintree.Subscription.create({
                "payment_method_token": the_token,
                "plan_id":PLAN_ID,
                })

            if subscription_result.is_success:
                payment_type = subscription_result.subscription.transactions[0].payment_instrument_type
                trans_id = subscription_result.subscription.transactions[0].id
                sub_id = subscription_result.subscription.id
                sub_amount = subscription_result.subscription.price

                if payment_type == braintree.PaymentInstrumentType.PayPalAccount:
                    newtrans = Transaction.objects.create_newtrans(
                    user=request.user,
                    transaction_id=trans_id,
                    amount=sub_amount,
                    card_type='paypal',)
                    trans_success = newtrans.success
                elif payment_type == braintree.PaymentInstrumentType.CreditCard:
                    credit_card_details = subscription_result.subscription.transactions[0].credit_card_details
                    card_type = credit_card_details.card_type
                    last_4 = credit_card_details.last_4
                    newtrans = Transaction.objects.create_newtrans(
                    user=request.user,
                    transaction_id=trans_id,
                    amount=sub_amount,
                    card_type=card_type,
                    last_four=last_4)
                    trans_success = newtrans.success
                else:
                    trans_success = False

                if trans_success:
                    membership_instance, created = Membership.objects.get_or_create(
                        user=request.user)
                    membership_date_update.send(
                        sender=membership_instance,
                        new_date_start=newtrans.timestamp,)
                    messages.success(request, 'Thanks for you support, now you become our site member, enjoy.')
                    # return HttpResponseRedirect(reverse('history'))
                    return redirect('history')
                else:
                    messages.error(request, 'There was an error with your trans, please contact us.')
                    return redirect('upgrade')
            else:
                error_ms = subscription_result.subscription.message
                messages.error(request, "An error occured: %s" % (error_ms))
                return redirect('upgrade')


        if member:
            become_member.send(sender=request.user,
                                month=str(month))
            messages.success(request, 'Hoho, now you become our site member, enjoy.')
            return HttpResponseRedirect(next_url)
        return render(request, 'billing/upgrade.html', context)
    return Http404

@login_required
def history(request):
    histories = request.user.transaction_set.get_success()
    return render(request, 'billing/history.html', {'queryset': histories})