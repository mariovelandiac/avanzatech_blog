from rest_framework.permissions import BasePermission

class IsSameUserOnCreate(BasePermission):
    """
    Custom permission to only allow users to create objects just for themselves.
    """
    def has_permission(self, request, view):
        # Check if the user making the request is the same as the user in the payload
        return request.data.get('user') == str(request.user.id)
