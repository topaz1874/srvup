from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from billing.models import Membership

class MyUserManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None):
        """
        Creates and saves a User with the given email, username
        and password.
        """
        if not username:
            raise ValueError("Username must be included")
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=255,
        unique=True,)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    is_member = models.BooleanField(default=False, verbose_name='Is Paid Member')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        if self.first_name:
            return self.first_name
        return self.username

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

       
#sender is the class of user
@receiver(user_logged_in)
def user_logged_in_handler(sender,request,signal,user, **kwargs):
    request.session.set_expiry(60000)
    # if there is a new user login then create membership obj
    membership_obj, created = Membership.objects.get_or_create(user=user)
    if created:
        membership_obj.date_start = timezone.now()
        membership_obj.save()
        user.is_member = True
        user.save()
    user.membership.update_status()


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser)
    bio = models.TextField(
        null=True,
        blank=True)
    facebook_link = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='facebook profile links')

    def __unicode__(self):
        return self.user.username

@receiver(post_save, sender=MyUser)
def profile_handler(sender,instance,created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)






    