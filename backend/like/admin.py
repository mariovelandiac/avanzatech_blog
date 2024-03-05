from django.contrib import admin
from like.models import Like
from django.contrib.admin import ModelAdmin

class LikeAdmin(ModelAdmin):
    # read
    list_display = ('user', 'post','is_active')
    search_fields = ('user', 'post')
    list_filter = ('user', 'post', 'is_active')
    readonly_fields = ('created_at','last_modified')
    ## create or edit
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Post', {'fields': ('post',)}),
        ('Active', {'fields': ('is_active',)}),  
    )

    


# Register your models here.
admin.site.register(Like, LikeAdmin)
