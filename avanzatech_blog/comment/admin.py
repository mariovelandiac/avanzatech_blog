from django.contrib import admin
from comment.models import Comment
from django.contrib.admin import ModelAdmin

class CommentAdmin(ModelAdmin):
    # read
    list_display = ('user', 'post','status')
    search_fields = ('user', 'post')
    list_filter = ('user', 'post', 'status')
    readonly_fields = ('created_at','last_modified')
    ## create or edit
    fieldsets = (
        ('Related to', {'fields': ('user','post')}),
        ('Content', {'fields': ('content',)}),
        ('Status', {'fields': ('status',)}),  
    )


# Register your models here.
admin.site.register(Comment, CommentAdmin)
