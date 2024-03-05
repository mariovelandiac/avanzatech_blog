from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .constants import ReadPermissions

def validate_user(user, serializer_self=None):
    authenticated_user = serializer_self.context['request'].user
    if user != authenticated_user:
        raise serializers.ValidationError("Invalid user in the payload.")
    return user

def check_read_permissions(user, post):
    # If is admin user
    if user.is_staff:
        return True

    # If team permission and user can't see the post
    if post.read_permission == ReadPermissions.TEAM and post.user.team.id != user.team.id:
        raise NotFound
        
    # If author permission and user isn't the author
    if post.read_permission == ReadPermissions.AUTHOR and post.user.id != user.id:
        raise NotFound

    return True