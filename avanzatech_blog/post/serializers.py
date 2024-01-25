from rest_framework import serializers
from post.constants import READ_PERMISSIONS
from post.models import Post

class PostListSerializer(serializers.ModelSerializer):
    read_permission = serializers.ChoiceField(choices=list(READ_PERMISSIONS.keys()))
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'user', 'read_permission']
        read_only_fields = ('id',)