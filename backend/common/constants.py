class AvailableCategories:
    """
    Constants for different categories of views.
    """
    PUBLIC = 'public'
    AUTHENTICATED = 'authenticated'
    TEAM = 'team'
    AUTHOR = 'author'

CATEGORIES = {
    AvailableCategories.PUBLIC: 'Anyone can access the post',
    AvailableCategories.AUTHENTICATED: 'Any authenticated user can access the post',
    AvailableCategories.TEAM: 'Any user on the same team as the post author can access the post',
    AvailableCategories.AUTHOR: 'Only the author can access the post',
}

class AvailablePermissions:
    """
    Constants for different permissions.
    """
    READ = 'read'
    EDIT = 'edit'
    NO_PERMISSION = 'no permission'

PERMISSIONS = {
    AvailablePermissions.READ: 'Can read the post',
    AvailablePermissions.EDIT: 'Can read and edit the post',
    AvailablePermissions.NO_PERMISSION: 'No permission to the post'
}

DEFAULT_ACCESS_CONTROL = {
    AvailableCategories.PUBLIC: AvailablePermissions.READ,
    AvailableCategories.AUTHENTICATED: AvailablePermissions.READ,
    AvailableCategories.TEAM: AvailablePermissions.EDIT,
    AvailableCategories.AUTHOR: AvailablePermissions.EDIT
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



