from django.contrib import admin
from post.models import Post
from django.contrib.admin import ModelAdmin

class PostAdmin(ModelAdmin):
    # read
    list_display = ('title', 'content','owner','read_permission', 'created_at','last_modified')
    search_fields = ('title', 'user')
    list_filter = ('title', 'user', 'read_permission')
    readonly_fields = ('created_at','last_modified')
    ## create or edit
    fieldsets = (
        ('Content', {'fields': ('title','content')}),
        ('Owner', {'fields': ('user',)}),
        ('Permission', {'fields': ('read_permission',)}),  
    )
    
    # Show owner instead of user
    def owner(self, obj):
        return obj.user.username    
    


# Register your models here.
admin.site.register(Post, PostAdmin)
