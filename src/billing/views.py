from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.core.urlresolvers import reverse
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

        # this part is test custome signal
        next_url = request.GET.get('next')
        member = request.POST.get('member')
        month = request.POST.get('month')
        if member:
            become_member.send(sender=request.user,
                                month=str(month))
            messages.success(request, 'Hoho, now you become our site member, enjoy.')
            return HttpResponseRedirect(next_url)

        try:
            #usermerchantid already created in userprofile post save handler
            merchant_obj = UserMerchantID.objects.get(user=request.user)
        except:
            messages.error(request, "There was an error with your account. Please contact us.")
            return redirect('contact_us')

        merchant_customer_id = merchant_obj.customer_id
        merchant_subscription_id = merchant_obj.subscription_id
        # merchant_plan_id = merchant_obj.plan_id

        # receive a payment method nonce from client
        # that means that server got customer's payment authorization
        if request.method == 'POST':
            nonce = request.POST.get('payment_method_nonce', None)
            if nonce is None:
                messages.error(request, "An error occured, please try again.")
                return redirect('upgrade')
            else:
                payment_method_result = braintree.PaymentMethod.create({
                    "customer_id": merchant_customer_id,
                    "payment_method_nonce": nonce,
                    "options": {
                        "make_default": True }
                    })
                if not payment_method_result.is_success:
                    messages.error(request, "An error occured: %s" % (payment_method_result.message))
                    return redirect('upgrade')

                the_token = payment_method_result.payment_method.token
                did_create_sub = False
                did_update_sub = False
                trans_success = False
                try:
                    current_subscription_result = braintree.Subscription.find(merchant_subscription_id)
                    current_subscription_status = current_subscription_result.status
                except:
                    current_subscription_result = None
                    current_subscription_status = None
                # if 1 then update subscription
                if current_subscription_result and current_subscription_status == "Active":
                    subscription_result = braintree.Subscription.update(merchant_subscription_id,{
                        "payment_method_token": the_token,
                        })
                    if subscription_result.is_success:
                        did_update_sub = True
                # create an subscription
                else:
                    subscription_result = braintree.Subscription.create({
                        "payment_method_token": the_token,
                        "plan_id":PLAN_ID,
                        })
                    if subscription_result.is_success:
                        did_create_sub = True

                if did_update_sub and not did_create_sub:
                    messages.success(request, "You've changed your subscription payment successed, thanks!")
                    # need to fixed if update had change membership time
                    return redirect('history')
                elif did_create_sub and not did_update_sub:
                    merchant_obj.subscription_id = subscription_result.subscription.id 
                    merchant_obj.plan_id = PLAN_ID
                    merchant_obj.save()

                    payment_type = subscription_result.subscription.transactions[0].payment_instrument_type
                    trans_id = subscription_result.subscription.transactions[0].id
                    sub_amount = subscription_result.subscription.price
                    # create new trans base on payment type
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
                else:
                    error_ms = subscription_result.message
                    messages.error(request, "An error occured: %s" % (error_ms))
                    return redirect('upgrade')
            
                # create membership obj and send update signal
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
                
        # send a client token 
        client_token = braintree.ClientToken.generate({
            "customer_id": merchant_customer_id
            })
        context = {'client_token':client_token}
        return render(request, 'billing/upgrade.html', context)
    return Http404

@login_required
def history(request):
    histories = request.user.transaction_set.get_success()
    return render(request, 'billing/history.html', {'queryset': histories})