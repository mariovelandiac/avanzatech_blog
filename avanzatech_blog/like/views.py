from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from like.models import Like
from like.serializers import LikeListCreateSerializer
from common.paginator import TwentyResultsSetPagination
from post.constants import ReadPermissions


class ListCreateLikeView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = TwentyResultsSetPagination
    serializer_class = LikeListCreateSerializer

    def perform_create(self, serializer):
        user_request = self.request.user
        post = serializer.validated_data.get('post')
        # If is admin user
        if user_request.is_staff:
            serializer.save(user=user_request)
            return
        self.check_read_permissions(post, user_request)
        serializer.save(user=user_request)
        

    def check_read_permissions(self, post, user):
        # If team permission and user can't see the post
        if post.read_permission == ReadPermissions.TEAM and post.user.team.id != user.team.id:
            raise NotFound
            
        # If author permission and user isn't the author
        if post.read_permission == ReadPermissions.AUTHOR and post.user.id != user.id:
            raise NotFound
