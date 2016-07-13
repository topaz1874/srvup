from django.contrib import admin
from .models import Notifications
# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender_object', 'target_object','action_object','recipient']

admin.site.register(Notifications, NotificationAdmin)
