from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from post.serializers import PostListSerializer

class PostListCreateView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    queryset = Post.objects.all()

    # Set the user field in the serializer to the user making the request
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)