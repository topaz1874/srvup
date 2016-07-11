from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .signals import notify
# Create your models here.
class NotificationQuerySet(models.query.QuerySet):
    def get_user(self, user):
        return self.filter(recipient=user)
    def read(self):
        return self.filter(read=True)

    def unread(self):
        return self.filter(unread=True)

class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def get_user(self,user):
        return self.get_queryset().get_user(user)

    def get_read(self,user):
        return self.get_queryset().read().get_user(user)

    def get_unread(self,user):
        return self.get_queryset().unread().get_user(user)




class Notifications(models.Model):
    sender_content_type = models.ForeignKey(ContentType, related_name='notify_sender')
    sender_object_id = models.PositiveIntegerField()
    sender_object = GenericForeignKey("sender_content_type", "sender_object_id")

    action_content_type = models.ForeignKey(ContentType, related_name='notify_action',
                                            null=True, blank=True)
    action_object_id = models.PositiveIntegerField(null=True, blank=True)
    action_object = GenericForeignKey("action_content_type", "action_object_id")

    target_content_type = models.ForeignKey(ContentType, related_name='notify_target',
                                            null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey("target_content_type", "target_object_id")

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
    verb = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    unread = models.BooleanField(default=True)
    read = models.BooleanField(default=False)

    objects = NotificationManager()

    def __unicode__(self):
        context = {
            'sender': self.sender_object,
            'action': self.action_object,
            'target': self.target_object,
            'recipient': self.recipient,
            'verb': self.verb,
        }
        return  "%(recipient)s : You've got %(verb)s from %(sender)s " % context

#  receiver functions
def new_notification(sender, **kwargs):
    """
    This receiver function will create a new notification instance
    with the signal sending from  comment create/reply view.
    """
    recipient = kwargs.pop('recipient')
    verb = kwargs.pop('verb')
    # create a new notification object
    new_note = Notifications(
        sender_content_type=ContentType.objects.get_for_model(sender),
        sender_object_id=sender.id,
        recipient=recipient,
        verb=verb,)

    for option in ("target", "action"):
        obj = kwargs.get(option,None)
        if obj:
            setattr(new_note, "%s_content_type" % (option), ContentType.objects.get_for_model(obj))
            setattr(new_note, "%s_object_id" % (option), obj.id)

    new_note.save()

# connect receiver to signal
notify.connect(new_notification)