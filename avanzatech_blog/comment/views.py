from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from comment.serializers import CommentListCreateSerializer, CommentDeleteSerializer
from comment.models import Comment
from common.utils import set_queryset_by_permissions
from common.mixins import DestroyMixin, PerformCreateMixin
from common.paginator import TenResultsSetPagination


class ListCreateCommentView(PerformCreateMixin, ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentListCreateSerializer
    pagination_class = TenResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('post', 'user')

    def get_queryset(self):
        user = self.request.user   
        queryset = set_queryset_by_permissions(user, Comment)
        return queryset

class DeleteCommentView(DestroyMixin, DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommentDeleteSerializer
    queryset = Comment.objects.all()

