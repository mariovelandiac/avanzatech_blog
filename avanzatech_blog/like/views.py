from rest_framework.generics import ListCreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from django_filters import rest_framework as filters
from like.models import Like
from like.serializers import LikeListCreateSerializer, LikeDeleteSerializer
from common.utils import set_queryset_by_permissions
from common.paginator import TwentyResultsSetPagination
from common.validators import check_read_permissions


class ListCreateLikeView(ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TwentyResultsSetPagination
    serializer_class = LikeListCreateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('post', 'user')
     
    def perform_create(self, serializer):
        user_request = self.request.user
        post = serializer.validated_data.get('post')
        check_read_permissions(user_request, post)
        serializer.save(user=user_request)
        
    def get_queryset(self):
        user = self.request.user   
        queryset = set_queryset_by_permissions(user, Like)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj
    

class DeleteLikeView(DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = LikeDeleteSerializer
    queryset = Like.objects.all()

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
        if self.request.user.is_staff:
            return Like.objects.all()
        return Like.objects.filter(user=self.request.user)
        

