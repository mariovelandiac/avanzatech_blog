from rest_framework import serializers
from comment.models import Comment
from common.validators import validate_user

class CommentListCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comment
        fields = ['id','content','user','username','post','is_active','created_at']
        read_only_fields = ('id','is_active','username','created_at')

    def validate_user(self, user):
        return validate_user(user, serializer_self=self)

class CommentDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id','user','post','is_active','created_at']
        read_only_fields = ('id','user','post','is_active','created_at')
