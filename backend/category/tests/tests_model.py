from django.test import TestCase
from category.models import Category
from category.tests.factories import CategoryFactory
from common.constants import AvailableCategories


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
        
    
    def test_all_categories_are_created(self): 
        # Arrange
        CategoryFactory.create_batch()
        # Act
        # Retrieve all categories from the database
        categories = Category.objects.all()
        # Assert
        # There are 4 categories in the database
        self.assertEqual(len(categories), 4)
        self.assertEqual(categories[0].name, AvailableCategories.PUBLIC)
        self.assertEqual(categories[1].name, AvailableCategories.AUTHENTICATED)
        self.assertEqual(categories[2].name, AvailableCategories.TEAM)
        self.assertEqual(categories[3].name, AvailableCategories.AUTHOR)