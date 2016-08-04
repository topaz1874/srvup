from django.contrib import admin

# Register your models here.
from .models import PageView

class PageViewAdmin(admin.ModelAdmin):
    list_filter = ('primary_content_type',)
    list_display = ['__unicode__', 'count', 'primary_content_type', 'primary_object_id', 'user']



admin.site.register(PageView, PageViewAdmin)