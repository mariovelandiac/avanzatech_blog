from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from .constants import ReadPermissions

'''
    This utility function allow to get a queryset based on the model, 
    the user and whether if the model is post related or not
'''
def set_queryset_by_permissions(user, model_class, is_related=True):
    queryset = model_class.objects.all()
    # User is admin
    if user.is_staff:
        return queryset

    # Related fields
    field_name = "read_permission"
    if is_related:
        field_name = "post__" + field_name
        queryset = queryset.filter(is_active=True)

    # Public posts
    if isinstance(user, AnonymousUser):
        return queryset.filter(**{f"{field_name}": ReadPermissions.PUBLIC})
    # User is authenticated and not admin
    else:
        filter_conditions = (
            Q(**{f"{field_name}__in": [ReadPermissions.PUBLIC, ReadPermissions.AUTHENTICATED]}) |
            Q(user_id=user.id, **{f"{field_name}": ReadPermissions.AUTHOR}) |
            Q(user__team=user.team, **{f"{field_name}": ReadPermissions.TEAM})
        )
        return queryset.filter(filter_conditions)

    