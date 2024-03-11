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
            fields = ['id','first_name','last_name','email','password']
            read_only_fields = ('id',)
            extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            email = validated_data.pop('email') # Extract the email from the data
            password = validated_data.pop('password')  # Extract the password from the data
            user = CustomUser.objects.create_user(email, password, **validated_data)  # Create a user instance with the validated data
            return user