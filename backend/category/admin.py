from django.contrib import admin
from category.models import Category
from django.contrib.admin import ModelAdmin

class CategoryAdmin(ModelAdmin):
    # read
    list_display = ('name', 'description')
    ## create or edit
    fieldsets = (
        ('Name', {'fields': ('name',)}),
        ('Description', {'fields': ('description',)}),
    )

# Register your models here.
admin.site.register(Category, CategoryAdmin)
