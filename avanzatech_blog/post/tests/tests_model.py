from django.test import TestCase
from post.tests.factories import PostFactory
from user.tests.factories import CustomUserFactory
from post.models import Post

# Create your tests here.
class PostModelTests(TestCase):

    def test_create_a_post_in_the_database_successfully(self):
        # Arrange
        post = PostFactory()
        # Act
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(post.id, post_db.id)
        self.assertEqual(post.title, post_db.title)
        self.assertEqual(post.user, post_db.user)
        self.assertEqual(post.content, post_db.content)
        self.assertEqual(post.created_at, post_db.created_at)
        self.assertEqual(post.last_modified, post_db.last_modified)
        self.assertEqual(post.read_permission, post_db.read_permission)

    def test_create_a_post_without_an_associated_user_should_raise_an_error(self):
        # Arrange
        data = {
            "title": "my_title",
            "content": "the content of the post",
            "read_permission": "public",
            "user": ""
        }
        # Act & Assert
        with self.assertRaises(ValueError):
            Post.objects.create(**data)

    def test_update_a_post_should_change_last_modified_date(self):
        # Arrange
        post = PostFactory()
        post_db = Post.objects.get(id=post.id)
        new_content = "new_content"
        post_db.content = new_content
        last_modified_date = post_db.last_modified
        # Act
        post_db.save()
        post_db_after_update = Post.objects.get(id=post.id)
        # Assert
        self.assertLess(last_modified_date, post_db_after_update.last_modified)
        self.assertEqual(post_db_after_update.content, new_content)
    
    def test_created_at_should_not_be_set_after_last_modified_after_a_update(self):
        # Arrange
        post = PostFactory()
        post_db = Post.objects.get(id=post.id)
        post_db.content = "new_content"
        # Act
        post_db.save()
        post_db_after_update = Post.objects.get(id=post.id)
        # Arrange
        self.assertLess(post_db_after_update.created_at, post_db_after_update.last_modified)

    def test_create_a_post_without_a_title_should_rise_an_error(self):
        # Arrange
        user = CustomUserFactory()
        data = {
            "user": user,
            "content": "the content of the post",
            "read_permission": "public"
        }
        # Act & Assert
        with self.assertRaises(ValueError):
            Post.objects.create(**data)


    def test_create_a_post_with_an_invalid_permission_should_rise_an_error(self):
        # Arrange
        user = CustomUserFactory()
        data = {
            "title": "post title",
            "user": user,
            "content": "the content of the post",
            "read_permission": "invalid permission"
        }
        # Act & Assert
        with self.assertRaises(ValueError):
            Post.objects.create(**data)
            posts = Post.objects.all()
            print(posts[0].read_permission)

    def test_create_a_post_with_an_invalid_user_should_raise_an_error(self):
        # Arrange
        user = {
            "id": 1,
            "email": "email@email.com",
            "password": "password",
            "team": 1
        }
        data = {
            "title": "my_title",
            "content": "the content of the post",
            "read_permission": "public",
            "user": user
        }
        # Act & Assert
        with self.assertRaises(ValueError):
            Post.objects.create(**data)
