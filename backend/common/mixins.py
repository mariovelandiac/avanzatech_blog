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
    def get_queryset_by_permissions(self, model_class, is_post_related=False):
        self.queryset = model_class.objects.all()
        # User is Admin
        if self.request.user.is_staff:
            return self.queryset

        # Related models
        self.__set_search_fields_by_model_relationship(is_post_related)
        
        # Anonymous user
        if isinstance(self.request.user, AnonymousUser):
            return self._get_queryset_for_anonymous_user()

        # Authenticated user
        return self._get_queryset_for_authenticated_user()

        
    def _get_queryset_for_anonymous_user(self):
        anonymous_conditions = {
            f"{self.post_field_name}__category__name": AccessCategory.PUBLIC,
        }
        # Set conditions by http method
        self.__set_conditions_by_http_method(anonymous_conditions)

        return self.queryset.filter(**anonymous_conditions)

    def _get_queryset_for_authenticated_user(self):
        # Public and Authenticated Posts
        non_owner_different_team_queryset = self._get_queryset_for_non_owner_different_team_posts()
        # Same Team Posts
        non_owner_same_team_queryset = self._get_queryset_for_non_owner_same_team_posts()
        # Owner Posts
        owner_queryset = self._get_queryset_for_owner_post()
        # Combine the querysets
        self.queryset = (owner_queryset | non_owner_same_team_queryset | non_owner_different_team_queryset)
        return self.queryset

    def _get_queryset_for_non_owner_different_team_posts(self):
        nodt_conditions = {
        f"{self.post_field_name}__category__name__in": [AccessCategory.PUBLIC, AccessCategory.AUTHENTICATED]
        }
        # Set conditions by http method
        self.__set_conditions_by_http_method(nodt_conditions)
        # Filter by contidionts
        nodt_queryset = self.queryset.filter(**nodt_conditions)
        # Exclude the user and the team
        nodt_queryset = nodt_queryset.exclude(**{
            f"{self.user_field_name}": self.request.user,
            f"{self.team_field_name}": self.request.user.team
        })
        return nodt_queryset
    
    def _get_queryset_for_non_owner_same_team_posts(self):
        # Basic conditions
        nost_conditions = {
            f"{self.post_field_name}__category__name": AccessCategory.TEAM,
            f"{self.team_field_name}": self.request.user.team
        }
        # Set conditions by HTTP Method
        self.__set_conditions_by_http_method(nost_conditions)
        # Filter by contidionts
        nost_queryset = self.queryset.filter(**nost_conditions)
        # Exclude the user
        nost_queryset = nost_queryset.exclude(**{
            f"{self.user_field_name}": self.request.user
        })
        return nost_queryset
    
    def _get_queryset_for_owner_post(self):
        # Basic conditions
        owner_conditions = {
            f"{self.post_field_name}__category__name": AccessCategory.AUTHOR,
            f"{self.user_field_name}": self.request.user
        }
        # Set conditions by HTTP Method
        self.__set_conditions_by_http_method(owner_conditions)
        # Filter by conditions
        return self.queryset.filter(**owner_conditions)
    
    def __set_conditions_by_http_method(self, conditions):
        if self.request.method in SAFE_METHODS:
            conditions[f"{self.post_field_name}__permission__name__in"] = [AccessPermission.READ, AccessPermission.EDIT]
        else:
            conditions[f"{self.post_field_name}__permission__name"] = AccessPermission.EDIT

    def __set_search_fields_by_model_relationship(self, is_post_related):
        self.user_field_name = "post__user" if is_post_related else "user"
        self.team_field_name = "post__user__team" if is_post_related else "user__team"
        self.post_field_name = "post_category_permission"
        if is_post_related:
            self.post_field_name = "post__" + self.post_field_name
            self.queryset = self.queryset.filter(is_active=True)


