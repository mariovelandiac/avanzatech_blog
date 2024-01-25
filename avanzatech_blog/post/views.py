from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from post.serializers import PostListSerializer

class PostListCreateView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    queryset = Post.objects.all()

