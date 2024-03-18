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

class CustomUserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(read_only=True, source='user.id')
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    team_id = serializers.IntegerField(read_only=True, source='user.team.id')
    is_admin = serializers.BooleanField(read_only=True, source='user.is_staff')

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')
        if password is None:
            raise serializers.ValidationError('A password is required to log in.')
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('A user with this email was not found.')
        return data
