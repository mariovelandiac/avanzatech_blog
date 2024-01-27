from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from like.models import Like
from like.serializers import LikeListCreateSerializer
from common.paginator import TwentyResultsSetPagination


class ListCreateLikeView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = TwentyResultsSetPagination
    serializer_class = LikeListCreateSerializer

    # Set the user field in the serializer to the user making the request
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
