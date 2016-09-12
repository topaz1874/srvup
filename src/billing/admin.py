from django.contrib import admin

from .models import Membership,Transaction,UserMerchantID
# Register your models here.

class UserMerchantAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer_id']

admin.site.register(Membership)
admin.site.register(Transaction)
admin.site.register(UserMerchantID, UserMerchantAdmin)