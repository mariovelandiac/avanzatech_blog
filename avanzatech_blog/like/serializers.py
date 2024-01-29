from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from like.models import Like
from common.constants import Status

class LikeListCreateUpdateSerializer(serializers.ModelSerializer):

    def validate_user(self, user):
        authenticated_user = self.context['request'].user
        if user != authenticated_user:
            raise serializers.ValidationError("Invalid user in the payload.")
        return user

    class Meta:
        model = Like
        fields = ['id','user','post','is_active']
        read_only_fields = ('id','is_active')

