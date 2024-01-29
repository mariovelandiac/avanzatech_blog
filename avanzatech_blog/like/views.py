from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from django_filters import rest_framework as filters
from like.models import Like
from like.serializers import LikeListCreateUpdateSerializer
from common.constants import ReadPermissions
from common.utils import set_queryset_by_permissions
from common.paginator import TwentyResultsSetPagination


class ListCreateUpdateLikeView(ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TwentyResultsSetPagination
    serializer_class = LikeListCreateUpdateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('post', 'user')
    
    def perform_create(self, serializer):
        user_request = self.request.user
        post = serializer.validated_data.get('post')
        # If is admin user
        if user_request.is_staff:
            serializer.save(user=user_request)
            return
        self._check_read_permissions(post, user_request)
        serializer.save(user=user_request)
        
    def get_queryset(self):
        user = self.request.user   
        queryset = set_queryset_by_permissions(user, Like)
        return queryset

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj
    
    def _check_read_permissions(self, post, user):
        # If team permission and user can't see the post
        if post.read_permission == ReadPermissions.TEAM and post.user.team.id != user.team.id:
            raise NotFound
            
        # If author permission and user isn't the author
        if post.read_permission == ReadPermissions.AUTHOR and post.user.id != user.id:
            raise NotFound
