from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.
from .models import Video,Category,TaggedItem,VoteUser

class TaggedItemInline(GenericTabularInline):
        '''
            Tabular Inline View for TaggedItem
        '''
        model = TaggedItem

class VoteUserInline(GenericTabularInline):
        '''
            Tabular Inline View for VoteUser
        '''
        model = VoteUser

class VideoInlin(admin.TabularInline):
    model = Video

class VideoAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline, VoteUserInline]
    list_display = ('title','share_message', 'active', 'featured', 'free_preview')
    # prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    inlines = [VideoInlin,TaggedItemInline]
    class Meta:
        model = Category

admin.site.register(Video, VideoAdmin)

admin.site.register(Category, CategoryAdmin)