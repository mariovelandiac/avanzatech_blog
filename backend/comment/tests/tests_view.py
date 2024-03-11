from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from post.tests.factories import PostFactory, PostCategoryPermissionFactory
from post.models import Post
from user.tests.factories import CustomUserFactory
from user.models import CustomUser
from team.tests.factories import TeamFactory
from comment.models import Comment
from comment.tests.factories import CommentFactory
from permission.tests.factories import PermissionFactory
from category.tests.factories import CategoryFactory
from common.constants import AccessCategory, AccessPermission, Status

class CommentCreateViewTests(APITestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.post = PostFactory(user=self.user)
        self.permissions = PermissionFactory.create_batch()
        self.categories = CategoryFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.READ,
            AccessCategory.AUTHOR: AccessPermission.READ
        }
        self.category_permission = PostCategoryPermissionFactory.create(post=self.post, category_permission=self.factory_category_permission)
        self.url = reverse('comment-list-create')

    def test_unauthenticated_user_can_not_create_a_comment_and_403_is_returned(self):
        # Arrange
        self.client.logout()
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": self.post.id
        }
        expected_comments = 0
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_create_a_comment_and_201_is_returned(self):
        # Arrange
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": self.post.id
        }
        expected_comments = 1
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_create_a_comment_and_comment_author_is_set_to_the_authenticated_user(self):
        # Arrange
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": self.post.id
        }
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.first()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db.user, self.user)

    def test_authenticated_user_can_create_a_comment_and_comment_post_is_set_to_the_post(self):
        # Arrange
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": self.post.id
        }
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.first()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db.post, self.post)

    def test_authenticated_user_can_not_create_a_comment_without_content_in_the_payload_and_400_is_returned(self):
        # Arrange
        data = {
            "content": "",
            "user": self.user.id,
            "post": self.post.id
        }
        expected_comments = 0
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_not_create_a_comment_without_user_in_the_payload_and_400_is_returned(self):
        # Arrange
        data = {
            "content": "Comment content",
            "user": "",
            "post": self.post.id
        }
        expected_comments = 0
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_not_create_a_comment_without_post_in_the_payload_and_400_is_returned(self):
        # Arrange
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": ""
        }
        expected_comments = 0
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_not_create_a_comment_without_user_and_post_in_the_payload_and_400_is_returned(self):
        # Arrange
        data = {
            "content": "Comment content",
            "user": "",
            "post": ""
        }
        expected_comments = 0
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_not_send_another_user_id_different_from_themselves_in_the_payload_and_400_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        data = {
            "content": "Comment content",
            "user": another_user.id,
            "post": self.post.id
        }
        expected_comments = 0
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_create_a_comment_in_a_post_with_edit_public_permissions_and_201_is_returned(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": post.id
        }
        expected_comments = 1
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_create_a_comment_in_a_post_with_no_public_permission_but_with_read_authenticated_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": post.id
        }
        expected_comments = 1
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_create_a_comment_in_a_post_without_public_permission_but_with_authenticated_read_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": post.id
        }
        expected_comments = 1
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_create_a_comment_in_a_post_with_only_team_access_and_201_is_returned(self):
        # Arrange
        post = PostFactory(user__team=self.team)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": post.id
        }
        expected_comments = 1
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_different_team_can_not_create_a_comment_in_post_with_only_team_access_and_404_is_returned(self):
        # Arrange
        another_team = TeamFactory()
        post = PostFactory(user__team=another_team)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": post.id
        }
        expected_comments = 0
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_can_create_a_comment_in_a_post_with_only_author_access_and_201_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": post.id
        }
        expected_comments = 1
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db, expected_comments)

    def test_authenticated_user_different_from_post_author_can_not_create_a_comment_in_post_with_only_author_access_and_404_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": post.id
        }
        expected_comments = 0
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(comment_db, expected_comments)

    def test_admin_user_can_create_a_comment_within_a_post_without_any_permission_and_201_is_returned(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        data = {
            "content": "Comment content",
            "user": admin_user.id,
            "post": post.id
        }
        expected_comments = 1
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db = Comment.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db, expected_comments)
        

    def test_authenticated_user_can_send_is_active_attribute_in_payload_but_is_ignored_by_default(self):
        # Arrange
        data = {
            "content": "Comment content",
            "user": self.user.id,
            "post": self.post.id,
            "is_active": False
        }
        expected_comments = 1
        # Act
        response = self.client.post(self.url, data, format='json')
        comment_db_count = Comment.objects.count()
        comment_db = Comment.objects.first()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db_count, expected_comments)
        self.assertTrue(comment_db.is_active)

class CommentListViewTests(APITestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.READ,
            AccessCategory.AUTHOR: AccessPermission.READ
        }
        self.url = reverse('comment-list-create')
        self.categories = CategoryFactory.create_batch()
        self.permissions = PermissionFactory.create_batch()

    def test_unauthenticated_user_can_list_comments_with_read_public_permission_and_200_is_returned(self):
        # Arrange
        self.client.logout()
        public_post = PostFactory()
        PostCategoryPermissionFactory.create(post=public_post, category_permission=self.factory_category_permission)
        authenticated_post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=authenticated_post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=public_post)
        CommentFactory.create_batch(5, post=authenticated_post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), public_post.id)
    
    def test_unauthenticated_user_can_not_list_comments_with_no_public_permission_and_200_is_returned(self):
        # Arrange
        self.client.logout()
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        expected_comments = 0
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)

    def test_authenticated_user_can_list_comments_with_just_read_public_permission_and_200_is_returned(self):
        # Arrange
        public_post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=public_post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=public_post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), public_post.id)

    def test_authenticated_user_can_list_comments_with_just_edit_public_permission_and_200_is_returned(self):
        # Arrange
        public_post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=public_post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=public_post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), public_post.id)

    def test_authenticated_user_can_list_comments_with_read_authenticated_permission_and_200_is_returned(self):
        # Arrange
        authenticated_post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=authenticated_post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=authenticated_post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), authenticated_post.id)

    def test_authenticated_user_can_list_comments_with_edit_authenticated_permission_and_200_is_returned(self):
        # Arrange
        authenticated_post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=authenticated_post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=authenticated_post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), authenticated_post.id)

    def test_authenticated_user_can_not_list_comments_with_any_public_or_authenticated_permission_and_200_is_returned(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        expected_comments = 0
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)

    def test_user_from_same_team_can_list_comments_with_team_read_permission_and_200_is_returned(self):
        # Arrange
        post = PostFactory(user__team=self.team)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), post.id)

    def test_user_from_different_team_can_not_list_comments_with_only_team_read_permission_and_200_is_returned(self):
        # Arrange
        another_team = TeamFactory()
        post = PostFactory(user__team=another_team)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        expected_comments = 0
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)

    def test_user_from_same_team_can_list_comments_with_team_edit_permission_and_200_is_returned(self):
        # Arrange
        post = PostFactory(user__team=self.team)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), post.id)

    def test_user_from_different_team_can_not_list_comments_with_only_team_edit_permission_and_200_is_returned(self):
        # Arrange
        another_team = TeamFactory()
        post = PostFactory(user__team=another_team)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        expected_comments = 0
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)

    def test_post_owner_can_list_comments_with_author_read_permission_and_200_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), post.id)

    def test_post_owner_can_list_comments_with_author_edit_permission_and_200_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), post.id)

    def test_admin_user_can_lists_comments_regardless_of_post_view_access(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        public_post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=public_post, category_permission=self.factory_category_permission)
        authenticated_post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=authenticated_post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=public_post)
        CommentFactory.create_batch(5, post=authenticated_post)
        expected_comments = 10
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)

    def test_authenticated_user_can_list_comments_and_they_are_returned_by_created_at_ascending_order(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        comment_1 = CommentFactory(post=post)
        comment_2 = CommentFactory(post=post)
        comment_3 = CommentFactory(post=post)
        expected_comments = [comment_1, comment_2, comment_3]
        # Act
        response = self.client.get(f"{self.url}?post={post.id}")
        results = response.data.get('results')
        comment_1_created_at = results[0].get('created_at')
        comment_2_created_at = results[1].get('created_at')
        comment_3_created_at = results[2].get('created_at')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(comment_1_created_at, comment_2_created_at)
        self.assertLess(comment_2_created_at, comment_3_created_at)

    def test_authenticated_user_can_filter_comments_by_post_id_and_200_is_returned(self):
        # Arrange
        post_1 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post_1)
        CommentFactory.create_batch(5, post=post_2)
        query_params = {
            "post": post_1.id
        }
        expected_comments = 5
        # Act
        response = self.client.get(self.url, query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('post'), post_1.id)

    def test_authenticated_with_same_team_user_can_filter_comments_by_user_id_and_200_is_returned(self):
        # Arrange
        user_1 = CustomUserFactory(team=self.team)
        user_2 = CustomUserFactory(team=self.team)
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, user=user_1, post=post)
        CommentFactory.create_batch(5, user=user_2, post=post)
        query_params = {
            "user": user_1.id
        }
        expected_comments = 5
        # Act
        response = self.client.get(self.url, query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('user').get('id'), user_1.id)

    def test_authenticated_user_can_filter_comments_by_post_id_and_user_id_and_200_is_returned(self):
        # Arrange
        user_1 = CustomUserFactory(team=self.team)
        user_2 = CustomUserFactory(team=self.team)
        post_1 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, user=user_1, post=post_1)
        CommentFactory.create_batch(5, user=user_2, post=post_2)
        query_params = {
            "user": user_1.id,
            "post": post_1.id
        }
        expected_comments = 5
        # Act
        response = self.client.get(self.url, query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)
        for result in results:
            self.assertEqual(result.get('user').get('id'), user_1.id)
            self.assertEqual(result.get('post'), post_1.id)

    def test_user_can_not_list_inactive_comments_and_200_is_returned(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        CommentFactory.create_batch(5, post=post)
        CommentFactory.create_batch(5, post=post, is_active=False)
        expected_comments = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_comments)

class CommentDeleteViewTests(APITestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.READ,
            AccessCategory.AUTHOR: AccessPermission.READ
        }
        self.categories = CategoryFactory.create_batch()
        self.permissions = PermissionFactory.create_batch()

    def test_unauthenticated_user_can_not_delete_a_comment_and_403_is_returned(self):
        # Arrange
        self.client.logout()
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        comment = CommentFactory(post=post)
        expected_comments = 1
        url = reverse('comment-delete', args=[comment.id])
        # Act
        response = self.client.delete(url)
        comment_db = Comment.objects.first()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), expected_comments)
        self.assertTrue(comment_db.is_active)

    def test_authenticated_user_can_soft_delete_a_comment_with_view_access_and_204_is_returned(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        comment = CommentFactory(post=post, user=self.user)
        expected_comments = 1
        url = reverse('comment-delete', args=[comment.id])
        # Act
        response = self.client.delete(url)
        comment_db = Comment.objects.count()
        comment_db_is_active = Comment.objects.first().is_active
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(comment_db, expected_comments)
        self.assertFalse(comment_db_is_active)

    def test_authenticated_user_can_not_soft_delete_a_comment_with_no_view_access_and_404_is_returned(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        comment = CommentFactory(post=post)
        expected_comments = 1
        url = reverse('comment-delete', args=[comment.id])
        # Act
        response = self.client.delete(url)
        comment_db = Comment.objects.count()
        comment_db_is_active = Comment.objects.first().is_active
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(comment_db, expected_comments)
        self.assertTrue(comment_db_is_active)

    def test_authenticated_user_can_not_soft_delete_a_comment_that_does_not_belong_to_current_user_and_404_is_returned(self):
        # Arrange
        another_user = CustomUserFactory()
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        comment = CommentFactory(post=post, user=another_user)
        expected_comments = 1
        url = reverse('comment-delete', args=[comment.id])
        # Act
        response = self.client.delete(url)
        comment_db = Comment.objects.count()
        comment_db_is_active = Comment.objects.first().is_active
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(comment_db, expected_comments)
        self.assertTrue(comment_db_is_active)

