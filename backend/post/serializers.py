from rest_framework import serializers
from post.models import Post, PostCategoryPermission
from user.serializers import CustomUserSerializer
from category.serialiazers import CategorySerializer
from permission.serializers import PermissionSerializer
class PostCategoryPermissionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    permission = PermissionSerializer()
    class Meta:
        model = PostCategoryPermission
        fields = ['category', 'permission']

class PostListCreateSerializer(serializers.ModelSerializer):
    categories_permission = PostCategoryPermissionSerializer(many=True, read_only=True)
    user = CustomUserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content','categories_permission','user','excerpt','created_at']
        read_only_fields = ('id','user','excerpt','created_at')
        extra_kwargs = {'content': {'write_only': True}}

class PostRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content','categories_permission','user','excerpt','created_at']
        read_only_fields = ('user','content','created_at')

