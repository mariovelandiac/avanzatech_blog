from rest_framework import serializers
from like.models import Like

class LikeListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id','user', 'post','status']
        read_only_fields = ('id','user','status')