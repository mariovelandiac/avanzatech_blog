from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from post.models import Post
from post.serializers import PostListCreateSerializer, PostRetrieveUpdateDestroySerializer
from common.constants import ReadPermissions
from common.utils import set_queryset_by_permissions
from common.paginator import TenResultsSetPagination


class ListCreatePostView(ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TenResultsSetPagination
    serializer_class = PostListCreateSerializer

    # Set the user field in the serializer to the user making the request
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self): 
        user = self.request.user   
        queryset = set_queryset_by_permissions(user, Post, self.request.method, is_related=False)
        return queryset
        

class RetrieveUpdateDeletePostView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostRetrieveUpdateDestroySerializer
            
    def get_queryset(self):
        user = self.request.user  
        method = self.request.method
        queryset = set_queryset_by_permissions(user, Post, method, is_related=False)
        return queryset




