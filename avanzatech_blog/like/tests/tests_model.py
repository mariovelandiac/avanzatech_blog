from django.test import TestCase
from like.tests.factories import LikeFactory
from like.models import Like
from user.tests.factories import CustomUserFactory
from post.tests.factories import PostFactory

class LikeModelTests(TestCase):

    def test_a_like_is_created_successfully_in_database(self):
        #Arrange
        like = LikeFactory()
        # Act
        like_db = Like.objects.get(id=like.id)
        # Assert
        self.assertEqual(like.id, like_db.id)
        self.assertEqual(like.user, like_db.user)
        self.assertEqual(like.post, like_db.post)
        self.assertEqual(like.status, like_db.status)
        self.assertEqual(like.created_at, like_db.created_at)
        self.assertEqual(like.last_modified, like_db.last_modified)

    def test_an_invalid_status_should_raise_an_error(self):
        #Arrange
        post = PostFactory()
        user = CustomUserFactory()
        like = {
            "user": user,
            "post": post,
            "status": "invalid"
        }
        # Act & Assert
        with self.assertRaises(ValueError):
            Like.objects.create(**like)

    def test_update_an_status_with_one_too_long_should_raise_an_error(self):
        #Arrange
        like = LikeFactory()
        like_db = Like.objects.get(id=like.id)
        like_db.status = "this status is way too long for the database options"
        # Act & Assert
        with self.assertRaises(ValueError):
            like_db.save()


    def test_create_a_like_with_an_invalid_user_should_raise_an_error(self):
        #Arrange
        post = PostFactory()
        user = {
            "id": 1,
            "email": "email@email.com",
            "password": "password",
            "team": 1
        }
        like = {
            "user": user,
            "post": post,
            "status": "invalid status"
        }
        # Act & Assert
        with self.assertRaises(ValueError):
            Like.objects.create(**like)

    def test_create_a_like_with_an_invalid_post_should_raise_an_error(self):
        #Arrange
        user = CustomUserFactory() 
        post = {
            "user": user,
            "content": "the content of the post",
            "read_permission": "public"
        }
        like = {
            "user": user,
            "post": post,
            "status": "invalid status"
        }
        # Act & Assert
        with self.assertRaises(ValueError):
            Like.objects.create(**like)

    def test_create_a_like_set_status_active_by_default(self):
        # Arrange
        like = LikeFactory()
        default_status = 'active'
        # Act
        like_db = Like.objects.get(id=like.id)
        # Assert
        self.assertEqual(like_db.status, default_status)

    def test_update_a_like_status_to_inactive_should_save_new_status_in_database(self):
        # Arrange
        like = LikeFactory()
        like_db = Like.objects.get(id=like.id)
        like_db.status = 'inactive'
        # Act
        like_db.save()
        # Assert
        like_db_updated = Like.objects.get(id=like.id)
        self.assertEqual(like_db_updated.status, 'inactive')
        self.assertLess(like.last_modified, like_db_updated.last_modified, "Last modified date not updated")

    def test_update_a_like_status_to_invalid_status_should_raise_an_error(self):
        # Arrange
        like = LikeFactory()
        like_db = Like.objects.get(id=like.id)
        like_db.status = 'invalid status'
        # Act & Assert
        with self.assertRaises(ValueError):
            like_db.save()

