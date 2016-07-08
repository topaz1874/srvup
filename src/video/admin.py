from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.
from .models import Video,Category,TaggedItem

class TaggedItemInline(GenericTabularInline):
        '''
            Tabular Inline View for TaggedItem
        '''
        model = TaggedItem

class VideoAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ('title','share_message', 'active', 'featured', 'free_preview')
    # prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    class Meta:
        model = Category

admin.site.register(Video, VideoAdmin)

admin.site.register(Category, CategoryAdmin)