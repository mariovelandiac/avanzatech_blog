from django.contrib import admin
from team.models import Team
from django.contrib.admin import ModelAdmin
from user.models import CustomUser

class CustomUserInline(admin.TabularInline):
    model = CustomUser
    extra = 0

class TeamAdmin(ModelAdmin):
    # read
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ## create or edit
    fieldsets = (
        ('Team''s Name', {'fields': ('name',)}),
    )

    inlines = [CustomUserInline]


# Register your models here.
admin.site.register(Team, TeamAdmin)
