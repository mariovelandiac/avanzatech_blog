from django.contrib import admin
from user.models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # read
    list_display = ('username','email', 'is_active', 'is_staff', 'is_superuser','team')
    search_fields = ('username', 'email', 'team')
    list_filter = ('is_active', 'is_staff', 'is_superuser','team')
    readonly_fields = ('last_login',)
    #Edit a user
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'email','password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Team', {'fields': ('team',)}),  
    )
    # Create a user
    add_fieldsets = (
        ("Create New User", {
            'classes': ('wide',),
            'fields': ('email', 'username','password1', 'password2', 'team'),
        }),
    )



# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
