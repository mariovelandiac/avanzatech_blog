from rest_framework import serializers
from user.models import CustomUser
from team.serializers import TeamSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name', 'team']

class CustomUserCreateSerializer(serializers.ModelSerializer):

        class Meta:
            model = CustomUser
            fields = ['id','email','password']
            read_only_fields = ('id',)
            extra_kwargs = {'password': {'write_only': True}}