from rest_framework.permissions import SAFE_METHODS
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from .constants import AccessCategory, AccessPermission

'''
    This utility function allow to get a queryset based on the model, 
    the user and whether if the model is post related or not. 
    This handle function needs models that implements the attribute is_active as a boolean attribute
'''
def set_queryset_by_permissions(user, model_class, method, is_related=True):
    # If you can read a post, then you can read the comments and the likes
    # If you can read and edit the post, then you can read and edit your comments and your likes
    # If you can't read and edit the post, then you can't read and edit the comments and the likes
    queryset = model_class.objects.all()
    # User is admin
    if user.is_staff:
        return queryset

    # Related models
    field_name = "post_category_permissions"
    if is_related:
        field_name = "post__" + field_name
        queryset = queryset.filter(is_active=True)

    # Check whether the http method is for read-only or not
    read_only = method in SAFE_METHODS
    
    # Public posts
    if isinstance(user, AnonymousUser):
        return _set_queryset_for_anonymous_user(queryset, field_name, safe_method=read_only)

    # Read: User is authenticated and not admin
    filter_conditions = (
        Q(**{f"{field_name}__in": [ReadPermissions.PUBLIC, ReadPermissions.AUTHENTICATED]}) |
        Q(user_id=user.id, **{f"{field_name}": ReadPermissions.AUTHOR}) |
        Q(user__team=user.team, **{f"{field_name}": ReadPermissions.TEAM})
    )
    return queryset.filter(filter_conditions)

def _set_queryset_for_anonymous_user(queryset, field_name, safe_method=True):
    filter_conditions = {
        f"{field_name}__category__name": AccessCategory.PUBLIC,
    }
    if safe_method:
        filter_conditions[f"{field_name}__permission__name__in"] = [AccessPermission.READ, AccessPermission.EDIT]
    else:
        filter_conditions[f"{field_name}__permission__name"] = AccessPermission.EDIT

    return queryset.filter(**filter_conditions)