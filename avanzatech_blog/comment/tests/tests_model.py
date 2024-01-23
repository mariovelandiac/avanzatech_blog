from django.test import TestCase
from common.constants import STATUS
from comment.tests.factories import CommentFactory
from comment.models import Comment
from post.models import Post
from user.tests.factories import CustomUserFactory
from post.tests.factories import PostFactory

# Create your tests here.
class CommentModelTests(TestCase):

    def test_create_a_comment_successfully_in_database(self):
        #Act
        comment = CommentFactory()
        comment_db = Comment.objects.get(id=comment.id)
        # Assert
        self.assertEqual(comment.user, comment_db.user)
        self.assertEqual(comment.post, comment_db.post)
        self.assertEqual(comment.content, comment_db.content)

    def test_a_comment_without_content_should_raise_an_error(self):
        # Act & Assert
        with self.assertRaises(ValueError):
            CommentFactory(content="")

    def test_a_comment_with_an_empty_user_should_raise_an_error(self):
        # Act & Assert
        with self.assertRaises(ValueError):
            CommentFactory(user="")
    
    def test_a_comment_with_an_empty_post_should_raise_an_error(self):
        # Act & Assert
        with self.assertRaises(ValueError):
            CommentFactory(user="")
        
    def test_a_comment_with_invalid_user_should_raise_an_error(self):
        # Arrange
        user = CustomUserFactory.build()
        # Act & Assert
        with self.assertRaises(ValueError):
            CommentFactory(user=user)
    
    def test_a_comment_with_invalid_post_should_raise_an_error(self):
        # Arrange
        post = PostFactory.build()
        # Act & Assert
        with self.assertRaises(ValueError):
            CommentFactory(post=post)

    def test_update_a_content_should_change_info_in_database(self):
        # Arrange
        comment = CommentFactory()
        comment_db = Comment.objects.get(id=comment.id)
        content = "new content updated"
        comment_db.content = content
        # Act
        comment_db.save()
        comment_updated = Comment.objects.get(id=comment.id)
        # Assert
        self.assertEqual(content, comment_updated.content)
        self.assertLess(comment.last_modified, comment_updated.last_modified)

    def test_delete_a_post_should_delete_the_current_comment(self):
        # Arrange
        comment = CommentFactory()
        current_comments = Comment.objects.count()
        expected_comments = 0
        post = Post.objects.get(pk=comment.post.pk)
        # Act
        post.delete()
        total_comments = Comment.objects.count()
        # Assert
        self.assertEqual(expected_comments, total_comments)
        self.assertNotEqual(current_comments, total_comments)


    def test_update_an_empty_status_should_raise_an_error(self):
        # Arrange
        comment = CommentFactory()
        comment_db = Comment.objects.get(pk=comment.pk)
        comment_db.status = ""
        # Act & Arrange
        with self.assertRaises(ValueError):
            comment_db.save()
        

    def test_update_a_invalid_status_should_raise_an_error(self):
        # Arrange
        comment = CommentFactory()
        comment_db = Comment.objects.get(pk=comment.pk)
        comment_db.status = "invalid"
        # Act & Arrange
        with self.assertRaises(ValueError):
            comment_db.save()

    def test_update_a_none_status_should_raise_an_error(self):
        # Arrange
        comment = CommentFactory()
        comment_db = Comment.objects.get(pk=comment.pk)
        comment_db.status = None
        # Act & Arrange
        with self.assertRaises(ValueError):
            comment_db.save()

    def test_update_a_valid_status_should_modify_status_in_database(self):
        # Arrange
        comment = CommentFactory()
        comment_db = Comment.objects.get(pk=comment.pk)
        new_status = 'inactive'
        comment_db.status = new_status
        # Act
        comment_db.save()
        comment_updated = Comment.objects.get(pk=comment.pk)
        # Assert
        self.assertEqual(comment_updated.status, new_status)






                

            