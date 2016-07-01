from django.contrib import admin

from .models import Comment
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'parent']
    class Meta:
        model = Comment
admin.site.register(Comment, CommentAdmin)