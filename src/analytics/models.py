from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
from .signals import page_view
class PageView(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True)
    path = models.CharField(max_length=256)
    timestamp = models.DateField(default=timezone.now())
    count = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        if self.user:
            return "%s: %s" % (self.user, self.path)
        return self.path

@receiver(page_view)
def page_view_handler(sender,path,**kwargs):
    # print "sender is : %s, kwargs are : %s" % (sender, kwargs)
    if sender.is_anonymous():
        new_page_view, created = PageView.objects.get_or_create(path=path, timestamp=timezone.now())
    else:
        new_page_view, created = PageView.objects.get_or_create(user=sender,path=path, timestamp=timezone.now())

    if not created:
        new_page_view.count += 1
        new_page_view.save()