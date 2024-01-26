# Permission Constant for Views
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