from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from post.models import Post
from post.serializers import PostListCreateSerializer, PostRetrieveUpdateDestroySerializer
from common.constants import ReadPermissions, DEFAULT_ACCESS_CONTROL
from common.mixins import GetQuerysetByPermissionsMixin
from common.paginator import TenResultsSetPagination


class ListCreatePostView(ListCreateAPIView, GetQuerysetByPermissionsMixin):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TenResultsSetPagination
    serializer_class = PostListCreateSerializer

    # Set the user field in the serializer to the user making the request
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self): 
        return self.get_queryset_by_permissions(Post, is_post_related=False)
        

class RetrieveUpdateDeletePostView(RetrieveUpdateDestroyAPIView, GetQuerysetByPermissionsMixin):

    permission_classes = [AllowAny]
    serializer_class = PostRetrieveUpdateDestroySerializer
            
    def get_queryset(self): 
        return self.get_queryset_by_permissions(Post, is_post_related=False)




