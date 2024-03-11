from rest_framework.generics import ListCreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from django_filters import rest_framework as filters
from like.models import Like
from like.serializers import LikeCreateSerializer, LikeListSerializer, LikeDeleteSerializer
from common.paginator import TwentyResultsSetPagination
from common.mixins import DestroyMixin, PerformCreateMixin, GetQuerysetByPermissionsMixin


class ListCreateLikeView(PerformCreateMixin, ListCreateAPIView, GetQuerysetByPermissionsMixin):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TwentyResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('post', 'user')
    
    def get_queryset(self): 
        return self.get_queryset_by_permissions(Like, is_post_related=True)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return LikeListSerializer
        return LikeCreateSerializer
    

class DeleteLikeView(DestroyMixin, DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = LikeDeleteSerializer
    queryset = Like.objects.all()
        
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

