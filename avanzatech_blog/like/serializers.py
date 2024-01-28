from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from like.models import Like
from common.constants import Status

class LikeListCreateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        post = data['post']
        user = data['user']
        # Check if an inactive like already exists for this post and user
        existing_like = Like.objects.filter(post=post, user=user).first()

        # If like does not exist
        if existing_like is None:
            authenticated_user = self.context['request'].user
            if user != authenticated_user:
                raise serializers.ValidationError("Invalid user in the payload.")
            return data
        # If like already exists
        if existing_like.is_active:
            raise serializers.ValidationError("Current like already exists and is active")
        else:
            # Update Like Status    
            data['is_active'] = True
            self.instance = existing_like
            return data


    class Meta:
        model = Like
        fields = ['id','user','post','is_active']
        read_only_fields = ('id','is_active')

