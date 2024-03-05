from django.contrib import admin
from post.models import Post, PostCategoryPermission
from django.contrib.admin import ModelAdmin, TabularInline

class PostCategoryPermissionInline(TabularInline):
    model = PostCategoryPermission
    extra = 4 
class PostAdmin(ModelAdmin):
    # read
    list_display = ('title', 'content','owner', 'excerpt','created_at','last_modified')
    search_fields = ('title', 'user')
    list_filter = ('title', 'user', 'read_permission')
    readonly_fields = ('created_at','last_modified')
    inlines = [PostCategoryPermissionInline]
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
