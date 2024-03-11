from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from django_filters import rest_framework as filters
from comment.serializers import CommentCreateSerializer, CommentListSerializer, CommentDeleteSerializer
from comment.models import Comment
from common.mixins import DestroyMixin, PerformCreateMixin, GetQuerysetByPermissionsMixin
from common.paginator import TenResultsSetPagination


class ListCreateCommentView(PerformCreateMixin, ListCreateAPIView, GetQuerysetByPermissionsMixin):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = TenResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('post', 'user')

    def get_queryset(self): 
        return self.get_queryset_by_permissions(Comment, is_post_related=True)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CommentListSerializer
        return CommentCreateSerializer

class DeleteCommentView(DestroyMixin, DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommentDeleteSerializer
    queryset = Comment.objects.all()

    


