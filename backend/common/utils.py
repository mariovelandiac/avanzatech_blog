from common.constants import AccessCategory, AccessPermission

def create_default_category_permissions_handler(categories, permissions):
    read_permission = next((p for p in permissions if p.name == AccessPermission.READ), None)
    edit_permission = next((p for p in permissions if p.name == AccessPermission.EDIT), None)

    category_permissions = []
    for category in categories:
        permission = read_permission if category.name in [AccessCategory.PUBLIC, AccessCategory.AUTHENTICATED] else edit_permission
        category_permissions.append({"category": category.id, "permission": permission.id})

    return category_permissions

def create_custom_category_permissions_handler(categories, permissions, custom_permissions):
    # custom_permission is a dictionary that indicates the permission for each category
    # This function creates de category_permission list with the corresponding ids
    category_permissions = []
    for category in categories:
        permission = next((p for p in permissions if p.name == custom_permissions[category.name]), None)
        category_permissions.append({"category": category.id, "permission": permission.id})
    return category_permissions