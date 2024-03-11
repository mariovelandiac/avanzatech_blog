from django.contrib import admin
from user.models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # read
    list_display = ('first_name','last_name','email','is_active','is_staff','is_superuser','team')
    search_fields = ( 'email', 'team')
    list_filter = ('is_active', 'is_staff', 'is_superuser','team')
    readonly_fields = ('last_login',)
    #Edit a user
    fieldsets = (
        ('Personal Info', {'fields': ('email','password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Team', {'fields': ('team',)}),  
    )
    # Create a user
    add_fieldsets = (
        ("Create New User", {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email','password1', 'password2','team'),
        }),
    )
    ordering = ['email']



# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
