from rest_framework import serializers
from common.constants import READ_PERMISSIONS, EXCERPT_LENGTH
from post.models import Post

class PostBaseSerializer(serializers.ModelSerializer):

    def create_or_update_excerpt(self):
        content = self.validated_data.get("content")
        if content is not None:
            excerpt = content[:EXCERPT_LENGTH] if len(content) > EXCERPT_LENGTH else content
            self.validated_data["excerpt"] = excerpt


class PostListCreateSerializer(PostBaseSerializer):
    read_permission = serializers.ChoiceField(choices=list(READ_PERMISSIONS.keys()))
    class Meta:
        model = Post
        fields = ['id','title', 'content','excerpt','user','read_permission','created_at']
        read_only_fields = ('id','user','excerpt','created_at')

class PostRetrieveUpdateDestroySerializer(PostBaseSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'excerpt','read_permission','user', 'last_modified']
        read_only_fields = ('last_modified','excerpt', 'user')
