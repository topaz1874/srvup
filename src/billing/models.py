from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from .signals import become_member

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

@receiver(models.signals.post_save, sender=Membership)
def post_save_handler(sender, instance, created, **kwargs):
    if not created: 
        instance.update_status()



