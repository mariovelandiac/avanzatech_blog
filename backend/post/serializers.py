from rest_framework import serializers
from post.models import Post, PostCategoryPermission
from user.serializers import CustomUserSerializer
from category.serialiazers import CategorySerializer
from category.models import Category
from permission.serializers import PermissionSerializer
from permission.models import Permission

class PostCategoryPermissionSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all())
    class Meta:
        model = PostCategoryPermission
        fields = ['category', 'permission']

class PostListCreateSerializer(serializers.ModelSerializer):
    category_permission = PostCategoryPermissionSerializer(many=True, source='post_category_permission')
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content','category_permission','user','excerpt','created_at']
        read_only_fields = ('id','excerpt','created_at')
        extra_kwargs = {'content': {'write_only': True}}

class PostRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    category_permission = PostCategoryPermissionSerializer(many=True, source='post_category_permission')
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','title','content','category_permission','user','created_at']
        read_only_fields = ('created_at',)

    def update(self, instance, validated_data):
        category_permission = validated_data.pop('post_category_permission', None)
        instance = super().update(instance, validated_data)
        if category_permission:
            existing_permissions = instance.post_category_permission.filter(post=instance)
            for cp in category_permission:
                category = cp['category']
                permission = cp['permission']
                if existing_permissions.filter(category=category).exists():
                    existing_permissions.filter(category=category).update(permission=permission)
        return instance

