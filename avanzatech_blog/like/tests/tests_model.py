from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from like.tests.factories import LikeFactory
from like.models import Like
from user.tests.factories import CustomUserFactory
from post.tests.factories import PostFactory
from post.models import Post

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
        self.assertEqual(like.is_active, like_db.is_active)
        self.assertEqual(like.created_at, like_db.created_at)
        self.assertEqual(like.last_modified, like_db.last_modified)

    def test_an_invalid_is_active_should_raise_an_error(self):
        #Arrange
        post = PostFactory()
        user = CustomUserFactory()
        like = {
            "user": user,
            "post": post,
            "is_active": "invalid"
        }
        # Act & Assert
        with self.assertRaises(ValidationError):
            Like.objects.create(**like)


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
            "is_active": "invalid is_active"
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
            "is_active": "invalid is_active"
        }
        # Act & Assert
        with self.assertRaises(ValueError):
            Like.objects.create(**like)

    def test_create_a_like_set_status_is_true_by_default(self):
        # Arrange
        like = LikeFactory()
        default_is_active = True
        # Act
        like_db = Like.objects.get(id=like.id)
        # Assert
        self.assertEqual(like_db.is_active, default_is_active)

    def test_update_a_like_is_active_to_inactive_should_save_new_is_active_in_database(self):
        # Arrange
        like = LikeFactory()
        like_db = Like.objects.get(id=like.id)
        like_db.is_active = False
        # Act
        like_db.save()
        # Assert
        like_db_updated = Like.objects.get(id=like.id)
        self.assertIs(like_db_updated.is_active, False)
        self.assertLess(like.last_modified, like_db_updated.last_modified, "Last modified date not updated")

    def test_update_a_like_status_to_invalid_is_active_should_raise_an_error(self):
        # Arrange
        like = LikeFactory()
        like_db = Like.objects.get(id=like.id)
        like_db.is_active = 'invalid is_active'
        # Act & Assert
        with self.assertRaises(ValidationError):
            like_db.save()

    def test_delete_a_post_should_delete_associated_like(self):
        # Arrange
        like = LikeFactory()
        post = Post.objects.get(pk=like.post.pk)
        current_likes = Like.objects.count()
        expected_likes = 0
        # Act
        post.delete()
        total_likes = Like.objects.all().count()
        # Assert
        self.assertEqual(total_likes, expected_likes)
        self.assertNotEqual(current_likes, total_likes)

    def test_create_two_likes_with_same_user_id_and_post_id_should_raise_an_error(self):
        # Arrange
        post = PostFactory()
        user = CustomUserFactory()
        like = LikeFactory(user=user, post=post)
        # Act & Assert
        with self.assertRaises(IntegrityError):
            LikeFactory(user=user, post=post)


