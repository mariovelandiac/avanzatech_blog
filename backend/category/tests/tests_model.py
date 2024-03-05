from django.test import TestCase
from category.models import Category

# Create your tests here.
class CategoryModelTests(TestCase):

    def test_retrieve_category_successfully(self):
        # Arrange
        # Create a category in the database
        category = Category.objects.create(name='Test Category')
        # Act
        # Retrieve the category from the database
        retrieved_category = Category.objects.get(name='Test Category')
        # Assert
        # The retrieved category is not None
        self.assertIsNotNone(retrieved_category)
        # The retrieved category has the correct name
        self.assertEqual(retrieved_category.name, 'Test Category')
        