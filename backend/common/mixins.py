from rest_framework.permissions import SAFE_METHODS
from rest_framework.generics import get_object_or_404
from django.db.models.query import QuerySet
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from common.validators import check_read_permissions
from common.constants import AccessCategory, AccessPermission

class PerformCreateMixin:

    def perform_create(self, serializer):
        user_request = self.request.user
        post = serializer.validated_data.get('post')
        check_read_permissions(user_request, post)
        serializer.save(user=user_request)

class DestroyMixin:
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(user=self.request.user)

class GetQuerysetByPermissionsMixin:

    '''
    This utility mixing allow to get a queryset based on the model, 
    the user and whether if the model is post related or not. 
    This handle function needs models that implements the attribute is_active as a boolean attribute
    '''
    def get_queryset_by_permissions(self, model_class, is_post_related=True):
        self.queryset = model_class.objects.all()
        # User is Admin
        if self.request.user.is_staff:
            return self.queryset

        # Related models
        self.user_field_name = "post__user" if is_post_related else "user"
        self.team_field_name = "post__user__team" if is_post_related else "user__team"
        self.search_field_name = "post_category_permission"
        if is_post_related:
            self.search_field_name = "post__" + self.search_field_name
            self.queryset = self.queryset.filter(is_active=True)
        
        # Anonymous user
        if isinstance(self.request.user, AnonymousUser):
            return self._set_queryset_for_anonymous_user()

        # Authenticated user
        return self._set_queryset_for_authenticated_user()

        
    def _set_queryset_for_anonymous_user(self):
        filter_conditions = {
            f"{self.search_field_name}__category__name": AccessCategory.PUBLIC,
        }
        # Read operations
        if self.request.method in SAFE_METHODS:
            filter_conditions[f"{self.search_field_name}__permission__name__in"] = [AccessPermission.READ, AccessPermission.EDIT]
        # Edit operations
        else:
            filter_conditions[f"{self.search_field_name}__permission__name"] = AccessPermission.EDIT

        return self.queryset.filter(**filter_conditions)

    def _set_queryset_for_authenticated_user(self):
        if self.request.method in SAFE_METHODS:
            return self._set_queryset_for_authenticated_user_reading()
        return self._set_queryset_for_authenticated_user_editing()

    def _set_queryset_for_authenticated_user_reading(self):
        # Public Posts
        read_public_post = Q(**{
            f"{self.search_field_name}__category__name": AccessCategory.PUBLIC,
            f"{self.search_field_name}__permission__name__in": [AccessPermission.READ, AccessPermission.EDIT],
        })
        # Authenticated Posts
        read_auth_post = Q(**{
            f"{self.search_field_name}__category__name": AccessCategory.AUTHENTICATED,
            f"{self.search_field_name}__permission__name__in": [AccessPermission.READ, AccessPermission.EDIT],
        })
        # Team Posts
        read_team_post = Q(**{
            f"{self.search_field_name}__category__name": AccessCategory.TEAM,
            f"{self.search_field_name}__permission__name__in": [AccessPermission.READ, AccessPermission.EDIT],
            f"{self.team_field_name}": self.request.user.team
        })
        # User Posts
        read_author_post = Q(**{
            f"{self.search_field_name}__category__name": AccessCategory.AUTHOR,
            f"{self.search_field_name}__permission__name__in": [AccessPermission.READ, AccessPermission.EDIT],
            f"{self.user_field_name}": self.request.user
        })
        # Exclude user conditions
        exclude_user_conditions = (read_public_post | read_auth_post | read_team_post)
        self.queryset.filter(exclude_user_conditions).exclude(**{f"{self.user_field_name}": self.request.user})

        # Add user specific post to the queryset
        self.queryset = (self.queryset | self.queryset.filter(read_author_post))
        return self.queryset

    def _set_queryset_for_authenticated_user_editing(self):
        # Public Posts
        edit_public_post = Q(**{
            f"{self.search_field_name}__category__name": AccessCategory.PUBLIC,
            f"{self.search_field_name}__permission__name": AccessPermission.EDIT,
        })
        # Authenticated Posts
        edit_auth_post = Q(**{
            f"{self.search_field_name}__category__name": AccessCategory.AUTHENTICATED,
            f"{self.search_field_name}__permission__name": AccessPermission.EDIT,
        })
        # Team Posts
        edit_team_post = Q(**{
            f"{self.search_field_name}__category__name": AccessCategory.TEAM,
            f"{self.search_field_name}__permission__name": AccessPermission.EDIT,
            f"{self.team_field_name}": self.request.user.team
        })
        # User Posts
        edit_author_post = Q(**{
            f"{self.search_field_name}__category__name": AccessCategory.AUTHOR,
            f"{self.search_field_name}__permission__name": AccessPermission.EDIT,
            f"{self.user_field_name}": self.request.user
        })
        # Exclude user conditions
        exclude_user_conditions = (edit_public_post | edit_auth_post | edit_team_post)
        self.queryset.filter(exclude_user_conditions).exclude(**{f"{self.user_field_name}": self.request.user})
        print("before adding user", self.queryset)
        print("is this the problem?", self.queryset.filter(edit_author_post))
        # Add user specific post to the queryset
        self.queryset = (self.queryset | self.queryset.filter(edit_author_post))
        print("after adding user", self.queryset)
        return self.queryset