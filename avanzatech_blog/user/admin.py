from django.contrib import admin
from user.models import CustomUser
from django.contrib.admin import ModelAdmin

class CustomUserAdmin(ModelAdmin):
    # read
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser','team')
    search_fields = ('email', 'team')
    list_filter = ('is_active', 'is_staff', 'is_superuser','team')
    ## create or edit
    fieldsets = (
        ('Personal Info', {'fields': ('email','password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Team', {'fields': ('team',)}),  
    )




# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
