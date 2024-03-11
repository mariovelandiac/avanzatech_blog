from rest_framework import serializers
from rest_framework.exceptions import NotFound
from common.constants import AccessCategory, AccessPermission

def validate_user(user, serializer_self=None):
    authenticated_user = serializer_self.context['request'].user
    if user != authenticated_user:
        raise serializers.ValidationError("Invalid user in the payload.")
    return user

def check_permissions(user, post):
    # Set parameters for access control
    # Boolean is admin user
    is_admin = user.is_staff
    # Boolean is the same owner of the post
    is_owner = post.user.id == user.id
    # Boolean is the same team of the post owner
    is_same_team = post.user.team.id == user.team.id

    # If is admin user
    if user.is_staff:
        return True

    # If is not the owner and not the same team
    if not is_owner and not is_same_team:
        return _check_permissions_for_public_and_authenticated_posts(user, post)

    # If is not the owner but the same team
    if not is_owner and is_same_team:
        return _check_permissions_for_same_team_posts(user, post)
        
    # If is the owner
    return _check_permissions_for_owner_post(user, post)

def _check_permissions_for_public_and_authenticated_posts(user, post):
    public_permissions = post.post_category_permission.filter(category__name=AccessCategory.PUBLIC).first()
    authenticated_permissions = post.post_category_permission.filter(category__name=AccessCategory.AUTHENTICATED).first()
    public_permissions_restricted = public_permissions.permission.name == AccessPermission.NO_PERMISSION
    authenticated_permissions_restricted = authenticated_permissions.permission.name == AccessPermission.NO_PERMISSION
    # If the post hasn't view access for public and authenticated users
    if public_permissions_restricted and authenticated_permissions_restricted:
        raise NotFound('Post not found')
    return True

def _check_permissions_for_same_team_posts(user, post):
    same_team_permissions = post.post_category_permission.filter(category__name=AccessCategory.TEAM).first()
    same_team_permissions_restricted = same_team_permissions.permission.name == AccessPermission.NO_PERMISSION
    # If the post hasn't view access for the same team
    if same_team_permissions_restricted:
        raise NotFound('Post not found')
    return True

def _check_permissions_for_owner_post(user, post):
    author_permissions = post.post_category_permission.filter(category__name=AccessCategory.AUTHOR).first()
    author_permissions_restricted = author_permissions.permission.name == AccessPermission.NO_PERMISSION
    # If the post hasn't view access for the author
    if author_permissions_restricted:
        raise NotFound('Post not found')
    return True
    


