import urllib2
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.utils.text import slugify
# Create your models here.
class VideoQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True)
    def active(self):
        return self.filter(active=True)

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def get_featured(self, free_preview=None):
        # return super(VideoManager, self).filter(featured=True)
        if free_preview:
            return self.get_queryset().featured().filter(free_preview=True)
        return self.get_queryset().featured().active()

    def all(self):
        return self.get_queryset().active()

DEFAULT_MESSAGE = """Check out this awesome video."""

class Video(models.Model):
    title = models.CharField(max_length=256)
    share_message = models.TextField(default=DEFAULT_MESSAGE, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, max_length=256)
    tags = GenericRelation("TaggedItem", null=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/%Y/%m/%d',null=True,blank=True)
    upload_vid = models.FileField(upload_to='uploads/%Y/%m/%d',null=True, blank=True)
    embed_code = models.CharField(max_length=500,null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    free_preview = models.BooleanField(default=False)
    category = models.ForeignKey("Category", null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateField(auto_now_add=False, auto_now=True, null=True)

    objects = VideoManager()

    class Meta:
        unique_together = ('slug', 'category')

    def __unicode__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Video,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'vid_slug': self.slug,
                                                'cat_slug':self.category.slug })
    def get_share_message(self):
        share_message = "%s %s" %(self.share_message, self.get_full_url())
        return urllib2.quote(share_message)

    def get_full_url(self):
        full_url ="%s%s" % (settings.MY_DOMAINS, self.get_absolute_url())
        return full_url

@receiver(post_save, sender=Video)
def vid_signal_post_save_receiver(sender,instance,created,**kwargs):
    print "signal sent" 
    if created:
        slugify_title = slugify(instance.title)
        new_slug = "%s %s" %(instance.title, str(instance.id))
        try:
            Video.objects.get(slug=slugify_title, category=instance.category)
            instance.slug = slugify(new_slug)
            instance.save()
            print "model exists, new slug generated"
        except Video.DoesNotExist:
            instance.slug = slugify_title
            instance.save()
            print "slug and model created"
        except Video.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
            instance.save()
            print "multiple model exists, new slug generated"
        except:pass
        

# post_save.connect(vid_signal_post_save_receiver, sender=Video)

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    tags = GenericRelation("TaggedItem", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category,self).save(*args,**kwargs)


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'cat_slug': self.slug })

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

TAG_CHOICES = (
    ('django','django'),
    ('python','python'),
    ('pycon', 'pycon'),
    ('css', 'css'),
    ('bootstrap','bootstrap'),
    ('content_types','content_types'),
    )

class TaggedItem(models.Model):
    tag = models.SlugField(choices=TAG_CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return self.tag




