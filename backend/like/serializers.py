from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from user.serializers import CustomUserSerializer
from like.models import Like
from common.constants import Status
from common.validators import validate_user

class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','user','post','is_active']
        read_only_fields = ('id','is_active')
    
    def validate_user(self, user):
        return validate_user(user, serializer_self=self)

    def run_validation(self, data=serializers.empty):
        # Check the payload
        post = data.get('post')
        user = data.get('user')
        if post is None or user is None:
            return super().run_validation(data)
        
        # Check if 'is_active' is False in the database
        like_in_db = Like.objects.filter(post=data['post'], user=data['user']).first()
        is_active_in_database = like_in_db and not like_in_db.is_active

        # If 'is_active' is False, skip uniqueness validation for user and post
        if is_active_in_database:
            self.fields['user'].validators = []
            self.fields['post'].validators = []
            self.instance = like_in_db
            self.instance.is_active = True
    
        return super().run_validation(data)

class LikeListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id','user','post','is_active']
        read_only_fields = ('id','user','post','is_active')


class LikeDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','user','post','is_active']
        read_only_fields = ('id','user','post','is_active')
