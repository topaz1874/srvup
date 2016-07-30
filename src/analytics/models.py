from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils import timezone

from video.models import Video,Category
from .signals import page_view

class PageViewQuerySet(models.QuerySet):
    def videos(self):
        primary_content_type = ContentType.objects.get_for_model(Video)
        return self.filter(primary_content_type=primary_content_type)

    def categories(self):
        primary_content_type = ContentType.objects.get_for_model(Category)
        return self.filter(primary_content_type=primary_content_type)


class PageViewManager(models.Manager):
    def get_queryset(self):
        return PageViewQuerySet(self.model, using=self._db)

    def get_videos(self):
        return self.get_queryset().videos()

    def get_categories(self):
        return self.get_queryset().categories()


class PageView(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True)
    path = models.CharField(max_length=256)
    timestamp = models.DateField(default=timezone.now)
    count = models.PositiveIntegerField(default=1)
    primary_content_type = models.ForeignKey(ContentType,related_name='primary_obj',
                                             null=True, blank=True)
    primary_object_id = models.PositiveIntegerField(null=True, blank=True)
    primary_content_object = GenericForeignKey('primary_content_type', 'primary_object_id')

    secondary_content_type = models.ForeignKey(ContentType,related_name='secondary_obj',
                                             null=True, blank=True)
    secondary_object_id = models.PositiveIntegerField(null=True, blank=True)
    secondary_content_object = GenericForeignKey('secondary_content_type', 'secondary_object_id')

    objects = PageViewManager()

    def __unicode__(self):
        if self.user:
            return "%s: %s" % (self.user, self.path)  
        return self.path

    class Meta:
        ordering = ['-timestamp']

@receiver(page_view)
def page_view_handler(sender,**kwargs):
    path = kwargs.get('path')

    if sender.is_anonymous():
        new_page_view, created = PageView.objects.get_or_create(path=path, timestamp=timezone.now())
    else:
        new_page_view, created = PageView.objects.get_or_create(user=sender,path=path, timestamp=timezone.now())
    
    for option in ("primary_obj", "secondary_obj"):
        obj = kwargs.get(option, None)
        if obj:
            name = option.split('_')[0]
            setattr(new_page_view, '%s_object_id' % (name), obj.id )
            setattr(new_page_view, '%s_content_type' % (name),\
                    ContentType.objects.get_for_model(obj))
            new_page_view.save()

    if not created:
        new_page_view.count += 1
        new_page_view.save()