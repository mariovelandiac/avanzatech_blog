from django.contrib import admin
from like.models import Like
from django.contrib.admin import ModelAdmin

class LikeAdmin(ModelAdmin):
    # read
    list_display = ('user', 'post','status')
    search_fields = ('user', 'post')
    list_filter = ('user', 'post', 'status')
    readonly_fields = ('created_at','last_modified')
    ## create or edit
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Post', {'fields': ('post',)}),
        ('Status', {'fields': ('status',)}),  
    )

    


# Register your models here.
admin.site.register(Like, LikeAdmin)
