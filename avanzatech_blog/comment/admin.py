from django.contrib import admin
from comment.models import Comment
from django.contrib.admin import ModelAdmin

class CommentAdmin(ModelAdmin):
    # read
    list_display = ('user', 'post','is_active')
    search_fields = ('user', 'post')
    list_filter = ('user', 'post', 'is_active')
    readonly_fields = ('created_at','last_modified')
    ## create or edit
    fieldsets = (
        ('Related to', {'fields': ('user','post')}),
        ('Content', {'fields': ('content',)}),
        ('Active', {'fields': ('is_active',)}),  
    )


# Register your models here.
admin.site.register(Comment, CommentAdmin)
