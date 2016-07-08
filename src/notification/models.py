from django.db import models
from django.conf import settings
from .signals import notify
# Create your models here.
class Notifications(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
    action = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return  str(self.action)

#  receiver functions
def new_notification(sender, recipient, action, **kwargs):
    print kwargs
    Notifications.objects.create(recipient=recipient, action=action)


# connect receiver to signal
notify.connect(new_notification)