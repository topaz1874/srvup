from django.utils import timezone
import braintree
import datetime

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    'q3m29r7tg2hj3fx3',
    'n7frpfxd8453gtn2',
    '15f9f94d97f31151598663137e05cfe1'
)

from .signals import membership_date_update

def check_membership_status(subscription_id):
    sub = braintree.Subscription.find(subscription_id)
    if sub.status == "Active":
        status = True
        next_billing_date = sub.next_billing_date
        small_time = datetime.time(0,0,1)
        datetime_obj = datetime.datetime.combine(next_billing_date, small_time)
        next_billing_date = timezone.make_aware(datetime_obj, timezone=None)
    else:
        status = False
        next_billing_date = None
    return status, next_billing_date

def update_braintree_memebership(user):
    subscription_id = user.usermerchantid.subscription_id
    membership = user.membership
    print 'membership date end :', membership.date_end
    if membership.date_end <= timezone.now() and subscription_id:
        status, next_billing_date = check_membership_status(subscription_id)
        membership_date_update.send(sender=membership, new_date_start=next_billing_date)
        print 'next_billing_date :', next_billing_date

    else:
        membership.update_status()


