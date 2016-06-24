from django.contrib import admin

# Register your models here.
from .models import Video,Category

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title','share_message', 'active', 'featured', 'free_preview')
    # prepopulated_fields = {'slug': ('title',)}

admin.site.register(Video, VideoAdmin)

admin.site.register(Category)