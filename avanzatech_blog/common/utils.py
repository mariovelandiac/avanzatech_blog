from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from .constants import ReadPermissions

'''
    This utility function allow to get a queryset based on the model, 
    the user and wheter if the model is post related or not
'''
def set_queryset_by_permissions(user, model_class, is_related=True):
    field_name = "read_permission"
    if is_related:
        field_name = "post__" + field_name
    # Public posts
    if isinstance(user, AnonymousUser):
        return model_class.objects.filter(**{f"{field_name}": ReadPermissions.PUBLIC})
    # User is admin
    elif user.is_staff:
        return model_class.objects.all()
    # User is authenticated and not admin
    else:
        filter_conditions = (
            Q(**{f"{field_name}__in": [ReadPermissions.PUBLIC, ReadPermissions.AUTHENTICATED]}) |
            Q(user_id=user.id, **{f"{field_name}": ReadPermissions.AUTHOR}) |
            Q(user__team=user.team, **{f"{field_name}": ReadPermissions.TEAM})
        )
        return model_class.objects.filter(filter_conditions)

    