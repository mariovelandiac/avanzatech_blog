from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from like.models import Like
from like.tests.factories import LikeFactory
from user.tests.factories import CustomUserFactory
from user.models import CustomUser
from post.tests.factories import PostFactory, PostCategoryPermissionFactory
from post.models import Post
from team.tests.factories import TeamFactory
from common.constants import AccessCategory, AccessPermission, CATEGORIES
from common.constants import Status
from category.tests.factories import CategoryFactory
from permission.tests.factories import PermissionFactory

class LikeCreateViewTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        CategoryFactory.create_batch()
        PermissionFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }
        self.data = {
            "user": self.user.id
        }
        self.url = reverse('like-list-create')
    
    def test_unauthenticated_user_can_not_create_a_like(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        self.data["post"] = post.id
        expected_likes = 0
        self.client.logout()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Like.objects.count(), expected_likes)

    def test_logged_in_user_can_not_create_more_than_one_like_to_one_post(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        self.data["post"] = post.id
        # Act
        response1 = self.client.post(self.url, self.data)
        response2 = self.client.post(self.url, self.data)
        expected_likes_db = 1
        # Assert
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_create_a_like_in_a_post_with_public_read_permission_post_and_not_authenticated_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id) # Created by the authenticated user
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
    
    def test_logged_in_user_can_create_a_like_in_a_post_with_public_edit_permission_post_and_not_authenticated_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id)

    def test_logged_in_user_can_create_a_like_in_a_post_with_authenticated_read_permission_post(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id)

    def test_logged_in_user_can_create_a_like_in_a_post_with_authenticated_edit_permission_post(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id)

    def test_logged_in_user_can_not_create_a_like_in_a_post_with_no_view_access_and_404_is_returned(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_create_a_like_in_a_same_team_post_with_team_read_permission_and_201_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_create_a_like_in_a_same_team_post_with_team_edit_permission_and_201_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_not_create_a_like_in_a_same_team_post_with_no_permission_and_404_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_create_a_like_in_a_post_with_author_read_permission_post(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_create_a_like_in_a_post_with_author_edit_permission_post(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_not_create_a_like_in_a_post_with_author_restricted_permission_post(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_a_logged_in_user_can_not_create_a_like_in_a_post_that_does_not_exist(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id + 1 # this post doesn't exist
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_invalid_data_returns_a_404_status_code(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        data = {
                "post_id": post.id,
                "user_id": self.user.id
                }
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_admin_user_can_create_a_like_in_a_post_with_public_no_permission_access_and_201_is_returned(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_admin_user_can_create_a_like_in_a_post_with_authenticated_no_permission_access_and_201_is_returned(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory()
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)


    def test_admin_user_can_create_a_like_in_a_post_with_public_and_authenticated_no_permission_access_and_201_is_returned(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_admin_user_can_create_a_like_in_a_post_with_team_no_permission_access_and_201_is_returned(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True, team=self.team)
        self.client.force_authenticate(admin_user)
        post = PostFactory(user__team=self.team)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_admin_user_can_create_a_like_in_a_post_with_just_author_read_access_and_201_is_returned(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(user=admin_user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_admin_user_can_create_a_like_in_a_post_with_just_author_edit_access_and_201_is_returned(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(user=admin_user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_admin_user_can_create_a_like_in_a_post_with_no_permissions_at_all_and_201_is_returned(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)


    def test_like_with_invalid_user_in_payload_should_return_400(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['user'] = other_user.id
        self.data['post'] = post.id
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_not_create_a_like_with_payload_inactive(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        self.data['post'] = post.id
        self.data['is_active'] = False
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        like_db_count = Like.objects.count()
        like_db = Like.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(like_db_count, expected_likes_db)
        self.assertIs(like_db.is_active, not self.data['is_active'])

    def test_a_logged_in_user_can_activate_like_if_has_view_access_to_the_post(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like = LikeFactory(user=self.user, post=post, is_active=False)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        like_db = Like.objects.get(id=like.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), expected_likes_db)
        self.assertIs(like_db.is_active, response.data['is_active'])

    def test_a_logged_in_user_can_not_activate_like_if_has_no_view_public_authenticated_access_to_the_post(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like = LikeFactory(user=self.user, post=post, is_active=False)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        like_db = Like.objects.get(id=like.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), expected_likes_db)
        self.assertFalse(like_db.is_active)

    def test_a_logged_in_user_can_activated_a_like_from_the_same_team_and_201_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like = LikeFactory(user=self.user, post=post, is_active=False)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        like_db = Like.objects.get(id=like.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), expected_likes_db)
        self.assertIs(like_db.is_active, response.data['is_active'])
        self.assertTrue(like_db.is_active)

    def test_a_logged_in_can_not_activate_a_like_from_the_same_team_if_post_has_not_view_access(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like = LikeFactory(user=self.user, post=post, is_active=False)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        like_db = Like.objects.get(id=like.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), expected_likes_db)
        self.assertFalse(like_db.is_active)

    def test_a_logged_in_user_can_activate_a_like_that_belongs_to_themselves_and_has_view_access_and_201_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like = LikeFactory(user=self.user, post=post, is_active=False)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        like_db = Like.objects.get(id=like.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), expected_likes_db)
        self.assertIs(like_db.is_active, response.data['is_active'])

    def test_a_logged_in_user_can_not_activated_a_like_that_belongs_to_themselves_and_has_no_view_access(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like = LikeFactory(user=self.user, post=post, is_active=False)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        like_db = Like.objects.get(id=like.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), expected_likes_db)
        self.assertFalse(like_db.is_active)

class LikeListViewTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.url = reverse('like-list-create')
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }
        CategoryFactory.create_batch()
        PermissionFactory.create_batch()

    def test_unauthenticated_user_can_list_only_public_likes_and_200_is_returned(self):
        # Arrange
        public_post = PostFactory()
        PostCategoryPermissionFactory.create(post=public_post, category_permission=self.factory_category_permission)
        non_public_post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=non_public_post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=public_post)
        LikeFactory.create_batch(3, post=non_public_post)
        expected_likes = 3
        # Act
        self.client.logout()
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_logged_in_user_can_list_likes_with_public_read_permission_and_not_authenticated_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_logged_in_user_can_list_likes_with_public_edit_permission_and_not_authenticated_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_logged_in_user_can_list_likes_with_non_public_permission_but_with_authenticated_read_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_logged_in_user_can_list_likes_with_non_public_permission_but_with_authenticated_edit_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_logged_in_user_can_not_list_likes_with_any_public_and_authenticated_permission(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 0
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_logged_in_user_can_list_likes_with_mixed_public_and_authenticated_permissions(self):
        # Arrange
        post_1 = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post_1)
        LikeFactory.create_batch(3, post=post_2)
        expected_likes = 6
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_same_team_user_can_list_likes_from_the_same_team_posts_with_team_read_permission(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_same_team_user_can_list_likes_from_the_same_team_with_team_edit_permission(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_same_team_user_can_list_likes_from_the_same_team_and_from_the_authenticated_posts(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post_1 = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post_1)
        LikeFactory.create_batch(3, post=post_2)
        expected_likes = 6
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_same_team_user_can_list_likes_from_the_same_team_and_from_themselves_posts(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post_1 = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post_1)
        LikeFactory.create_batch(3, post=post_2)
        expected_likes = 6
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_same_team_user_can_not_lists_likes_from_the_same_team_if_they_do_not_have_view_access(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        post_with_authenticated_access = PostFactory()
        PostCategoryPermissionFactory.create(post=post_with_authenticated_access, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        LikeFactory.create_batch(3, post=post_with_authenticated_access)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)
    
    def test_logged_in_user_can_list_likes_from_public_authenticated_same_team_and_from_themselves_posts(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post_1 = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        post_3 = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_3, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post_1)
        LikeFactory.create_batch(3, post=post_2)
        LikeFactory.create_batch(3, post=post_3)
        expected_likes = 9
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_post_owner_with_read_permission_can_list_likes_from_themselves_and_200_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_post_owner_with_edit_permission_can_list_likes_from_themselves_and_200_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 3
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_post_owner_without_permission_can_not_list_likes_from_themselves_and_200_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post)
        expected_likes = 0
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_user_without_any_like_available_to_see_will_receive_empty_list(self):
        # Arrange
        user = CustomUserFactory()
        self.client.force_authenticate(user)
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(10, post=post)
        expected_count = 0
        #  Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_admin_user_can_list_every_like_regardless_of_the_posts_permissions(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(5, post=post)
        expected_likes = 5
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), expected_likes)

    def test_admin_user_can_list_self_likes(self):
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post_1 = PostFactory(user=admin_user)
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory(user=admin_user)
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        LikeFactory(post=post_1, user=admin_user)
        LikeFactory(post=post_2, user=admin_user)
        expected_count = 2
        #  Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for like in results:
            self.assertEqual(admin_user.id, like.get('user').get('id'))

    def test_listing_likes_returns_the_entire_user_and_the_team_name_of_each_user(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like = LikeFactory(post=post)
        expected_count = 1
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        self.assertEqual(results[0]['user']['id'], like.user.id)
        self.assertEqual(results[0]['user']['first_name'], like.user.first_name)
        self.assertEqual(results[0]['user']['last_name'], like.user.last_name)
        self.assertEqual(results[0]['user']['team']['name'], like.user.team.name)
    
    def test_unauthenticated_user_can_filter_public_likes_by_user_id(self):
        # Arrange
        self.client.logout()
        other_user = CustomUserFactory()
        post_1 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        LikeFactory(post=post_1, user=self.user)
        LikeFactory(post=post_1, user=other_user)
        LikeFactory(post=post_2, user=self.user)
        LikeFactory(post=post_2, user=other_user)
        query_params = {
            'user': self.user.id,
        }
        expected_count = 2
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for like in results:
            user_db = CustomUser.objects.get(id=like['user']['id'])
            self.assertEqual(user_db.id, self.user.id)

    def test_unauthenticated_user_can_filter_public_likes_by_post_id(self):
        # Arrange
        self.client.logout()
        post_public = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_public, category_permission=self.factory_category_permission)
        post_private = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create(post=post_private, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post_public)
        LikeFactory.create_batch(3, post=post_private)
        query_params = {
            'post': post_public.id,
        }
        expected_count = 3
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_unauthenticated_user_can_filter_public_likes_by_user_id_and_post_id(self):
        # Arrange
        self.client.logout()
        other_user = CustomUserFactory()
        post_public = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post_public, category_permission=self.factory_category_permission)
        post_2 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        like = LikeFactory(post=post_public, user=self.user)
        LikeFactory.create_batch(3, post=post_2) 
        LikeFactory.create_batch(3, post=post_public) 
        query_params = {
            'user': self.user.id,
            'post': post_public.id
        }
        expected_count = 1
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['user']['id'], self.user.id)
        self.assertEqual(results[0]['post'], post_public.id)

    def test_logged_in_user_can_filter_public_and_authenticated_likes_by_user_id(self):
        # Arrange
        other_user = CustomUserFactory()
        post_1 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        LikeFactory(post=post_1, user=self.user)
        LikeFactory(post=post_1, user=other_user)
        LikeFactory(post=post_2, user=self.user)
        LikeFactory(post=post_2, user=other_user)
        query_params = {
            'user': self.user.id,
        }
        expected_count = 2
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for like in results:
            user_db = CustomUser.objects.get(id=like.get('user').get('id'))
            self.assertEqual(user_db.id, self.user.id)

    def test_logged_in_user_can_filter_public_and_authenticated_likes_by_post_id(self):
        # Arrange
        other_user = CustomUserFactory()
        post_1 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory()
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post_1)
        LikeFactory.create_batch(3, post=post_2)
        query_params = {
            'post': post_1.id,
        }
        expected_count = 3
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for like in results:
            self.assertEqual(like['post'], post_1.id)

    def test_logged_in_user_can_filter_public_likes_by_user_id_and_post_id(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like = LikeFactory(post=post, user=self.user)
        LikeFactory.create_batch(3, post=post)
        query_params = {
            'user': self.user.id,
            'post': post.id
        }
        expected_count = 1
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['user']['id'], self.user.id)
        self.assertEqual(results[0]['post'], post.id)

    def test_same_team_user_can_filter_likes_from_posts_id_and_will_see_likes_from_same_team_users_and_others_users_with_post_access(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post, user__team=self.team)
        LikeFactory.create_batch(3, post=post)
        query_params = {
            'post': post.id,
        }
        expected_count = 6
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)


    def test_unauthenticated_user_only_can_list_active_public_post_likes(self):
        # Arrange
        self.client.logout()
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post, is_active=True)
        LikeFactory.create_batch(3, post=post, is_active=False)
        expected_count = 3
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for like in results:
            self.assertTrue(like['is_active'])


    def test_logged_in_user_only_can_list_active_public_and_authenticated_post_likes(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post, is_active=True)
        LikeFactory.create_batch(3, post=post, is_active=False)
        expected_count = 3
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for like in results:
            self.assertTrue(like['is_active'])

    def test_logged_in_user_can_only_list_active_same_team_likes(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        post = PostFactory(user=another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post, is_active=True, user__team=self.team)
        LikeFactory.create_batch(3, post=post, is_active=False, user__team=self.team)
        expected_count = 3
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for like in results:
            post_db = Post.objects.get(id=like['post'])
            self.assertIs(like['is_active'], True)
            self.assertEqual(post_db.user.team.id, self.team.id)

    def test_owner_of_a_post_user_can_only_list_active_author_likes(self):
        # Arrange
        post_1 = PostFactory(user=self.user)
        PostCategoryPermissionFactory.create(post=post_1, category_permission=self.factory_category_permission)
        post_2 = PostFactory(user=self.user)
        PostCategoryPermissionFactory.create(post=post_2, category_permission=self.factory_category_permission)
        LikeFactory(user=self.user, post=post_1, is_active=True)
        LikeFactory(user=self.user, post=post_2, is_active=False)
        expected_count = 1
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        self.assertEqual(results[0]['user']['id'], self.user.id)

    def test_admin_user_can_list_active_and_inactive_likes(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        LikeFactory.create_batch(3, post=post, is_active=True)
        LikeFactory.create_batch(3, post=post, is_active=False)
        expected_count = 6
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_post_are_listed_by_last_modified_order_most_new_at_first_and_so_on(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory.create(post=post, category_permission=self.factory_category_permission)
        like_1 = LikeFactory(post=post, is_active=True)
        like_2 = LikeFactory(post=post, is_active=True)
        like_3 = LikeFactory(post=post, is_active=True)
        expected_order = [like_3.id, like_2.id, like_1.id]
        # Act
        response = self.client.get(self.url)
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(results[0]['id'], expected_order[0])
        self.assertEqual(results[1]['id'], expected_order[1])
        self.assertEqual(results[2]['id'], expected_order[2])


class LikeDeleteViewTests(APITestCase):

    def setUp(self):
        self.permissions = PermissionFactory.create_batch()
        self.categories = CategoryFactory.create_batch()
        self.team = TeamFactory()
        self.user = CustomUserFactory()
        self.post = PostFactory()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.READ,
            AccessCategory.AUTHOR: AccessPermission.READ
        }
        self.category_permission = PostCategoryPermissionFactory.create(post=self.post, category_permission=self.factory_category_permission)
        self.like = LikeFactory(user=self.user, post=self.post)
        self.client.force_authenticate(self.user)
        self.url = reverse('like-delete', kwargs={"user": self.user.id, "post": self.post.id})


    def test_unauthenticated_user_can_not_soft_delete_a_active_public_like(self):
        # Assert
        self.client.logout()
        # Act
        response = self.client.delete(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_logged_in_user_can_soft_delete_a_like_created_by_themselves(self):
        # Arrange
        expected_count = 1
        # Act
        response = self.client.delete(self.url)
        # Assert
        like_db_count = Like.objects.count()
        like_db = Like.objects.filter(id=self.like.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(len(like_db), 0)
        self.assertEqual(like_db_count, expected_count)
        self.assertFalse(like_db[0].is_active)


    def test_logged_in_user_can_not_soft_delete_like_created_by_other_user(self):
        # Arrange
        other_user = CustomUserFactory()
        self.client.force_authenticate(other_user)
        expected_count = 1
        # Act
        response = self.client.delete(self.url)
        # Assert
        like_db_count = Like.objects.count()
        like_db = Like.objects.filter(id=self.like.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(len(like_db), 0)
        self.assertEqual(like_db_count, expected_count)
        self.assertTrue(like_db[0].is_active)


    def test_admin_user_can_soft_delete_any_like_regardless_of_permissions(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        expected_count = 1
        # Act
        response = self.client.delete(self.url)
        # Assert
        like_db_count = Like.objects.count()
        like_db = Like.objects.filter(id=self.like.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(len(like_db), 0)
        self.assertEqual(like_db_count, expected_count)
        self.assertFalse(like_db[0].is_active)

    def test_logged_in_user_can_not_soft_delete_like_with_invalid_lookup_fields_post_invalid(self):
        # Arrange
        url = reverse('like-delete', kwargs={"user": self.user.id, "post": (self.post.id + 1)}) # This post does not exists
        expected_count = 1
        like_db = Like.objects.filter(user=self.user.id, post=self.post.id+1)
        # Act
        response = self.client.delete(url)
        # Assert
        like_db_count = Like.objects.count()
        like_db = Like.objects.filter(id=self.like.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(len(like_db), 0)
        self.assertEqual(like_db_count, expected_count)
        self.assertTrue(like_db[0].is_active)

    def test_logged_in_user_can_not_soft_delete_like_with_invalid_lookup_fields_user_invalid(self):
        # Arrange
        url = reverse('like-delete', kwargs={"user": self.user.id + 1, "post": self.post.id}) # This user does not exists
        expected_count = 1
        like_db = Like.objects.filter(user=self.user.id, post=self.post.id+1)
        # Act
        response = self.client.delete(url)
        # Assert
        like_db_count = Like.objects.count()
        like_db = Like.objects.filter(id=self.like.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(len(like_db), 0)
        self.assertEqual(like_db_count, expected_count)
        self.assertTrue(like_db[0].is_active)





        
        
 