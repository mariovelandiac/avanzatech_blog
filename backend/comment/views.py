from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from comment.serializers import CommentListCreateSerializer, CommentDeleteSerializer
from comment.models import Comment
from common.mixins import DestroyMixin, PerformCreateMixin, GetQuerysetByPermissionsMixin
from common.paginator import TenResultsSetPagination


class ListCreateCommentView(PerformCreateMixin, ListCreateAPIView, GetQuerysetByPermissionsMixin):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentListCreateSerializer
    pagination_class = TenResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('post', 'user')

    def get_queryset(self): 
        return self.get_queryset_by_permissions(Comment, is_post_related=True)

class DeleteCommentView(DestroyMixin, DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommentDeleteSerializer
    queryset = Comment.objects.all()

    


