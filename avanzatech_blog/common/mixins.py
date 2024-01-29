from rest_framework.generics import get_object_or_404
from django.db.models.query import QuerySet
from common.validators import check_read_permissions

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

    def get_object(self):
        user_request = self.request.user
        # Check the kwargs
        user_kwargs = self.kwargs.get('user')
        post_kwargs = self.kwargs.get('post')
        if user_kwargs is None or post_kwargs is None:
            raise NotFound

        # Find object
        filter_kwargs = {
            'user': user_kwargs,
            'post': post_kwargs
        }
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj

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