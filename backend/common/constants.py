class AccessCategory:
    """
    Constants for different categories of views.
    """
    PUBLIC = 'public'
    AUTHENTICATED = 'authenticated'
    TEAM = 'team'
    AUTHOR = 'author'

CATEGORIES = {
    AccessCategory.PUBLIC: 'Anyone can access the post',
    AccessCategory.AUTHENTICATED: 'Any authenticated user can access the post',
    AccessCategory.TEAM: 'Any user on the same team as the post author can access the post',
    AccessCategory.AUTHOR: 'Only the author can access the post',
}

class AccessPermission:
    """
    Constants for different permissions.
    """
    READ = 'read'
    EDIT = 'edit'
    NO_PERMISSION = 'no permission'

PERMISSIONS = {
    AccessPermission.READ: 'Can read the post',
    AccessPermission.EDIT: 'Can read and edit the post',
    AccessPermission.NO_PERMISSION: 'No permission to the post'
}

DEFAULT_ACCESS_CONTROL = {
    AccessCategory.PUBLIC: AccessPermission.READ,
    AccessCategory.AUTHENTICATED: AccessPermission.READ,
    AccessCategory.TEAM: AccessPermission.EDIT,
    AccessCategory.AUTHOR: AccessPermission.EDIT
}

class Status:
    """
    Constants for different status values.
    """
    ACTIVE = True
    INACTIVE = False

STATUS = {
    Status.ACTIVE: "resource is active",
    Status.INACTIVE: "resource is not active"
}

STATUS_CHOICES = [(status, description) for (status, description) in STATUS.items()]

EXCERPT_LENGTH = 200
WORDS_MOCK_TEXT = 100

CONTENT_MOCK = "If you really want to hear about it, the first thing you'll probably want to know is where I was born, and what my lousy childhood was like, and how my parents were occupied and all before they had me, and all that David Copperfield kind of crap, but I don't feel like going into it."


class ReadPermissions:
    PUBLIC = 'public'
    AUTHENTICATED = 'authenticated'
    TEAM = 'team'
    AUTHOR = 'author'

# Permission Constant for Models
READ_PERMISSIONS = {
    ReadPermissions.PUBLIC: 'Public: Anyone can access the post',
    ReadPermissions.AUTHENTICATED: 'Authenticated: any authenticated user can access the post',
    ReadPermissions.TEAM: 'Team: Any user on the same team as the post author can access the post',
    ReadPermissions.AUTHOR: 'Author: Only the author can access the post',
}



