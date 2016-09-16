from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from billing.models import Membership,UserMerchantID

import braintree

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    'q3m29r7tg2hj3fx3',
    'n7frpfxd8453gtn2',
    '15f9f94d97f31151598663137e05cfe1'
)

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
        membership_obj, created = Membership.objects.get_or_create(user=instance)
        if created:
            membership_obj.date_start = timezone.now()
            membership_obj.save()
            instance.is_member = True
            instance.save()
        instance.membership.update_status()

    try:
        merchant_obj = UserMerchantID.objects.get(user=instance)
    except:
        #create a new braintree customer
        new_customer_result = braintree.Customer.create({
            "email": instance.email
            })
        #customer successed record customer id to UserMerchantID table
        if new_customer_result.is_success:
            merchant_customer_id = new_customer_result.customer.id
            merchant_obj, created = UserMerchantID.objects.get_or_create(
                user=instance,
                customer_id=merchant_customer_id)
            print """Customer created with id = {0}""".format(new_customer_result.customer.id)
        else:
            print """Error: {0}""".format(new_customer_result.message)


        


    