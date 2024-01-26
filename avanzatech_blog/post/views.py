from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from post.models import Post
from post.serializers import PostListCreateSerializer, PostRetrieveUpdateDestroySerializer
from post.constants import ReadPermissions
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
        # List Public posts
        if isinstance(user, AnonymousUser):
            return Post.objects.filter(read_permission=ReadPermissions.PUBLIC)
        # User is admin
        if user.is_staff:
            return Post.objects.all()
        # User is authenticated and not admin
        filter_conditions = Q(read_permission__in=[ReadPermissions.PUBLIC, ReadPermissions.AUTHENTICATED]) | Q(user_id=user.id, read_permission=ReadPermissions.AUTHOR) | Q(user__team=user.team, read_permission=ReadPermissions.TEAM)
        return Post.objects.filter(filter_conditions)
        

class RetrieveUpdateDeletePostView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostRetrieveUpdateDestroySerializer

    def get_queryset(self):
        user = self.request.user   
        # List Public posts
        if isinstance(user, AnonymousUser):
            return Post.objects.filter(read_permission=ReadPermissions.PUBLIC)
        return Post.objects.all()
    
    # Check if the user making the request is the owner of the object
    def get_object(self):
        user = self.request.user
        # Here is executed get_queryset()
        obj = super().get_object()
        # Admin is requesting
        if user.is_staff:
            return obj
        # Edit and Delete permission
        if user != obj.user and self.request.method not in SAFE_METHODS:
            raise PermissionDenied("You do not have permission to perform this action.")
        # Team permission but not in the same Team
        if obj.read_permission == ReadPermissions.TEAM and obj.user.team != user.team:
            raise NotFound
        # Author Permission but not the same author
        if obj.read_permission == ReadPermissions.AUTHOR and obj.user != user:
            raise NotFound
        return obj


