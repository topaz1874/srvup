import random

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from .signals import become_member,membership_date_update

# Create your models here.
class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_start = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.user.username

    def update_status(self):
        if self.date_end >= timezone.now():
            self.user.is_member = True
            self.user.save()
        elif self.date_end < timezone.now():
            self.user.is_member = False
            self.user.save()
        else:pass 

@receiver(become_member)
def become_member_handler(sender, **kwargs):
    user = sender
    month = kwargs.get('month')
    if month:
        user.membership.date_end += relativedelta(months=int(month))
        user.membership.save()
        user.membership.update_status()

@receiver(membership_date_update)
def membership_date_update_handler(sender, new_date_start, **kwargs):
    membership = sender
    current_date_end = membership.date_end
    if current_date_end >= new_date_start:
        membership.date_end += relativedelta(months=1)
    else:
        membership.date_start = new_date_start
        membership.date_end = new_date_start + relativedelta(months=1)
    membership.save()
    membership.update_status()


@receiver(models.signals.post_save, sender=Membership)
def post_save_handler(sender, instance, created, **kwargs):
    if not created: 
        instance.update_status()


class TransactionQuerySet(models.QuerySet):
    def success(self):
        return self.filter(success=True)

class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)

    def get_success(self):
        return self.get_queryset().success()

    def create_newtrans(self, user, transaction_id, amount, card_type,\
        last_four=None, success=None, transaction_status=None):
        if not user:
            raise ValueError("User must be added.")
        if not transaction_id:
            raise ValueError("Must completed a transaction to add an new.")

        new_order_id = "%s%s%s" % (transaction_id[:2], random.randint(1,9), transaction_id[2:])
        newtrans = self.model(
            user=user,
            transaction_id=transaction_id,
            amount=amount,
            card_type=card_type,
            order_id = new_order_id)
        if last_four is not None:
            newtrans.last_four = last_four
        if success is not None:
            newtrans.success = success
            newtrans.transaction_status = transaction_status

        newtrans.save(using=self._db)
        return newtrans


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    transaction_id = models.CharField(max_length=256) #braintree or stripe
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    card_type = models.CharField(max_length=256) #paypal
    last_four = models.PositiveIntegerField(null=True, blank=True)
    success = models.BooleanField(default=True) #if fail then status log errors
    transaction_status = models.CharField(max_length=256, null=True, blank=True)
    order_id = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = TransactionManager()

    def __unicode__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']








