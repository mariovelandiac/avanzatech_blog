from rest_framework.generics import ListCreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from like.models import Like
from like.serializers import LikeListCreateSerializer, LikeDeleteSerializer
from common.utils import set_queryset_by_permissions
from common.paginator import TwentyResultsSetPagination
from common.mixins import DestroyMixin, PerformCreateMixin


class ListCreateLikeView(PerformCreateMixin, ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TwentyResultsSetPagination
    serializer_class = LikeListCreateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('post', 'user')
    
        
    def get_queryset(self):
        user = self.request.user   
        queryset = set_queryset_by_permissions(user, Like)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj
    

class DeleteLikeView(DestroyMixin, DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = LikeDeleteSerializer
    queryset = Like.objects.all()
        

