from rest_framework import serializers
from permission.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']
        read_only_fields = ('name',)