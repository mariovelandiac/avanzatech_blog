from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from post.models import Post
from post.serializers import PostListCreateSerializer, PostRetrieveUpdateDestroySerializer

class ListCreatePostView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostListCreateSerializer
    queryset = Post.objects.all()

    # Set the user field in the serializer to the user making the request
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RetrieveUpdateDeletePostView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostRetrieveUpdateDestroySerializer
    queryset = Post.objects.all()

    # Check if the user making the request is the owner of the object
    def get_object(self):
        obj = super().get_object()

        if self.request.user.is_staff:
            return obj

        if self.request.user != obj.user:
            raise PermissionDenied("You do not have permission to perform this action.")

        return obj