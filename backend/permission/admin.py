from django.contrib import admin
from permission.models import Permission
from django.contrib.admin import ModelAdmin

class PermissionAdmin(ModelAdmin):
    # read
    list_display = ('name', 'description')
    ## create or edit
    fieldsets = (
        ('Name', {'fields': ('name',)}),
        ('Description', {'fields': ('description',)}),
    )

# Register your models here.
admin.site.register(Permission, PermissionAdmin)
