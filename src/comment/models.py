from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import truncatechars
from account.models import MyUser
from video.models import Video
# Create your models here.
class CommentQuerySet(models.QuerySet):
    def all(self):
        return self.filter(active=True).filter(parent=None)

    # def recent(self, user):
    #     return self.filter(active=True).filter(author=user).filter(parent=None)[:3]
    
    def recent(self):
        try:
            recent_num = settings.DISPLAY_RECENT_COMMENTS_NUM
        except:
            recent_num = 3

        return self.filter(active=True).filter(parent=None)[:recent_num]


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def get_recent(self):
        return self.get_queryset().recent()

    def create_comment(self, text=None, author=None, video=None, path=None, parent=None):
        if not path:
            raise ValueError("must include a path when adding comment")
        if not author:
            raise ValueError("who are you? Must include a user when adding comment")

        comment = self.model(
            text=text,
            author=author,
            path=path)
        if video is not None:
            comment.video=video
        if parent is not None:
            comment.parent=parent
        comment.save(using=self._db)
        return comment



class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey('account.MyUser')
    parent = models.ForeignKey('self', null=True, blank=True)
    video = models.ForeignKey(Video, null=True, blank=True)
    path = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    active = models.BooleanField(default=True)

    objects = CommentManager()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['-timestamp']

    @property
    def get_preview(self):
        return truncatechars(self.text, 60)
        
    @property
    def get_comment(self):
        return self.text

    @property
    def is_child(self):
        if self.parent is not None:return True
        else: return False

    @property
    def get_children(self):
        if self.is_child:
            return None
        else:
            return Comment.objects.filter(parent=self)

    @property
    def get_origin(self):
        return self.path

    def get_absolute_url(self):
        return reverse('comment_thread', kwargs={'pk':self.id})

    @property
    def get_affected_users(self):
        """just loop through children comment and return all users"""
        children_comment = self.get_children
        if children_comment:
            users = []
            for child in children_comment:
                if  child.author not in users:
                    users.append(child.author)
            return users
        return None


