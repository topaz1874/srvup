from django.contrib import admin

from .models import Membership,Transaction
# Register your models here.
admin.site.register(Membership)
admin.site.register(Transaction)
