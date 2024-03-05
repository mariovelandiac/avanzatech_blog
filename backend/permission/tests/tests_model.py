from django.test import TestCase
from permission.models import Permission
from permission.tests.factories import PermissionFactory
from common.constants import AvailablePermissions

# Create your tests here.
class PermissionModelTests(TestCase):

    def test_retrieve_permission_successfully(self):
        # Arrange
        # Create a permission in the database
        permission = Permission.objects.create(name='Test Permission')
        # Act
        # Retrieve the permission from the database
        retrieved_permission = Permission.objects.get(name='Test Permission')
        # Assert
        # The retrieved permission is not None
        self.assertIsNotNone(retrieved_permission)
        # The retrieved permission has the correct name
        self.assertEqual(retrieved_permission.name, 'Test Permission')
    
    def test_all_permissions_are_created(self):
        # Arrange
        PermissionFactory.create_batch()
        # Act
        # Retrieve all permissions from the database
        permissions = Permission.objects.all()
        # Assert
        # There are 4 permissions in the database
        self.assertEqual(len(permissions), 3)
        self.assertEqual(permissions[0].name, AvailablePermissions.READ)
        self.assertEqual(permissions[1].name, AvailablePermissions.EDIT)
        self.assertEqual(permissions[2].name, AvailablePermissions.NO_PERMISSION)
        