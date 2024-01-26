from rest_framework import serializers
from post.constants import READ_PERMISSIONS
from post.models import Post

class PostListCreateSerializer(serializers.ModelSerializer):
    read_permission = serializers.ChoiceField(choices=list(READ_PERMISSIONS.keys()))
    class Meta:
        model = Post
        fields = ['id','title', 'content','user','read_permission','created_at']
        read_only_fields = ('id','user','created_at')

class PostRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'read_permission','user', 'last_modified']
        read_only_fields = ('last_modified', 'user')
