from django import forms
from django.contrib import admin
from post.models import Post, PostCategoryPermission
from django.contrib.admin import ModelAdmin, TabularInline
from category.models import Category
from permission.models import Permission

class PostCategoryPermissionInline(TabularInline):
    model = PostCategoryPermission
    extra = 4
    max_num = 4

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "permission":
            kwargs["widget"] = admin.widgets.AdminRadioSelect  # Use radio buttons for permissions
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        FormSet = super().get_formset(request, obj, **kwargs)
        class CustomFormSet(FormSet):
            def clean(self):
                super().clean()
                categories = Category.objects.all()
                permissions_selected = [form.cleaned_data.get('permission') for form in self.forms]
                if None in permissions_selected:
                    raise forms.ValidationError("Please select a permission for every category.")
        return CustomFormSet

    def has_delete_permission(self, request, obj=None):
        return False

class PostAdmin(ModelAdmin):
    # read
    list_display = ('title','owner', 'excerpt','created_at','last_modified')
    search_fields = ('title', 'user')
    list_filter = ('title', 'user',)
    readonly_fields = ('created_at','last_modified')
    inlines = [PostCategoryPermissionInline]
    ## create or edit
    fieldsets = (
        ('Content', {'fields': ('title','content')}),
        ('Owner', {'fields': ('user',)}), 
    )
    
    # Show owner instead of user
    def owner(self, obj):
        return obj.user.username    
    

# Register your models here.
admin.site.register(Post, PostAdmin)
