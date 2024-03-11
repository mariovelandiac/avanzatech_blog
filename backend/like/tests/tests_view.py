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

# class LikeListViewTests(APITestCase):

#     def setUp(self):
#         self.team = TeamFactory()
#         self.user = CustomUserFactory(team=self.team)
#         self.client.force_authenticate(self.user)
#         self.url = reverse('like-list-create')

#     def test_unauthenticated_user_can_see_only_public_likes(self):
#         # Arrange
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR)
#         expected_count = 2
#         self.client.logout()
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             post_db = Post.objects.get(id=like['post'])
#             self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)

#     def test_logged_in_user_can_list_likes_with_public_and_authenticated_associated_post(self):
#         # Arrange
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED)
#         expected_count = 4
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_logged_in_user_only_can_see_likes_with_team_permission_by_the_same_team(self):
#         # Arrange
#         other_team = TeamFactory()
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user__team=self.team)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user__team=other_team)
#         expected_count = 2
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             user_db = CustomUser.objects.get(id=like['user'])
#             self.assertEqual(user_db.team.id, self.team.id)

#     def test_logged_in_user_only_can_see_likes_with_author_permission_post_by_the_same_author(self):
#         # Arrange
#         other_user = CustomUserFactory()
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=other_user)
#         expected_count = 2
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             user_db = CustomUser.objects.get(id=like['user'])
#             self.assertEqual(user_db.id, self.user.id)

#     def test_logged_in_user_can_list_likes_with_team_permission_post_but_not_author_by_the_same_user(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user=other_user)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=other_user)
#         expected_count = 2
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Response
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             post_db = Post.objects.get(id=like['post'])
#             self.assertEqual(post_db.read_permission, ReadPermissions.TEAM)

#     def test_logged_in_user_can_list_public_authenticated_team_and_self_likes(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user=other_user)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user)
#         expected_count = 8
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_logged_in_user_can_list_team_and_self_likes(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         LikeFactory.create_batch(1, post__read_permission=ReadPermissions.TEAM, user=self.user)
#         LikeFactory.create_batch(1, post__read_permission=ReadPermissions.TEAM, user=other_user)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user)
#         expected_count = 4
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_user_without_any_like_available_to_see_will_receive_empty_list(self):
#         # Arrange
#         user = CustomUserFactory()
#         self.client.force_authenticate(user)
#         LikeFactory.create_batch(10, post__read_permission=ReadPermissions.AUTHOR, user=self.user)
#         expected_count = 0
#         #  Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_admin_user_can_list_every_like_regardless_of_the_posts_permissions(self):
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR)
#         expected_count = 8
#         #  Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_admin_user_can_list_self_likes(self):
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         LikeFactory.create_batch(3, user=admin_user)
#         expected_count = 3
#         #  Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             self.assertEqual(admin_user.id, like['user'])

#     def test_unauthenticated_user_can_filter_public_likes_by_user_id(self):
#         # Arrange
#         self.client.logout()
#         other_user = CustomUserFactory()
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=other_user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=other_user)
#         query_params = {
#             'user': self.user.id,
#         }
#         expected_count = 3
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             post_db = Post.objects.get(id=like['post'])
#             userd_db = CustomUser.objects.get(id=like['user'])
#             self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)
#             self.assertEqual(userd_db.id, self.user.id)

#     def test_unauthenticated_user_can_filter_public_likes_by_post_id(self):
#         # Arrange
#         self.client.logout()
#         post_public = PostFactory(read_permission=ReadPermissions.PUBLIC)
#         LikeFactory.create_batch(3, post=post_public)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED)

#         query_params = {
#             'post': post_public.id,
#         }
#         expected_count = 3
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             post_db = Post.objects.get(id=like['post'])
#             self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)

#     def test_unauthenticated_user_can_filter_public_likes_by_user_id_and_post_id(self):
#         # Arrange
#         self.client.logout()
#         other_user = CustomUserFactory()
#         post_public = PostFactory(read_permission=ReadPermissions.PUBLIC)
#         like = LikeFactory(post=post_public, user=self.user)
#         LikeFactory.create_batch(3, post=post_public) 
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
#         query_params = {
#             'user': self.user.id,
#             'post': post_public.id
#         }
#         expected_count = 1
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['user'], self.user.id)
#         self.assertEqual(results[0]['post'], post_public.id)
#         post_db = Post.objects.get(id=results[0]['post'])
#         self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)

#     def test_logged_in_user_can_filter_public_and_authenticated_likes_by_user_id(self):
#         # Arrange
#         other_user = CustomUserFactory()
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=other_user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=other_user)
#         query_params = {
#             'user': self.user.id,
#         }
#         expected_count = 6
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             user_db = CustomUser.objects.get(id=like['user'])
#             self.assertEqual(user_db.id, self.user.id)

#     def test_logged_in_user_can_filter_public_and_authenticated_likes_by_post_id(self):
#         # Arrange
#         other_user = CustomUserFactory()
#         post_auth = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
#         LikeFactory.create_batch(3, post=post_auth)
#         LikeFactory.create_batch(3)

#         query_params = {
#             'post': post_auth.id,
#         }
#         expected_count = 3
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             self.assertEqual(like['post'], post_auth.id)

#     def test_logged_in_user_can_filter_public_likes_by_user_id_and_post_id(self):
#         # Arrange
#         other_user = CustomUserFactory()
#         post_public = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
#         like = LikeFactory(post=post_public, user=self.user)
#         LikeFactory.create_batch(3, post=post_public) 
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
#         query_params = {
#             'user': self.user.id,
#             'post': post_public.id
#         }
#         expected_count = 1
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['user'], self.user.id)
#         self.assertEqual(results[0]['post'], post_public.id)

#     def test_logged_in_user_can_filter_likes_by_user_id(self):
#         # Arrange
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user) 
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user=self.user) 
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user) 
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user) 
#         LikeFactory.create_batch(7)
#         query_params = {
#             'user': self.user.id,
#         }
#         expected_count = 10
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             self.assertEqual(like['user'], self.user.id)

#     def test_logged_in_user_can_filter_likes_by_post_id_with_team_permission_post(self):
#         # Arrange
#         post = PostFactory(read_permission=ReadPermissions.TEAM, user__team=self.team)
#         LikeFactory.create_batch(3, post=post, user__team=self.team) 
#         LikeFactory.create_batch(3)
#         query_params = {
#             'post': post.id,
#         }
#         expected_count = 3
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             post_db = Post.objects.get(id=like['post'])
#             self.assertEqual(post_db.read_permission, ReadPermissions.TEAM)

#     def test_logged_in_user_can_filter_likes_by_post_id_with_author_permission_post(self):
#         # Arrange
#         post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=self.user)
#         LikeFactory(post=post, user=self.user) 
#         LikeFactory.create_batch(3)
#         query_params = {
#             'post': post.id,
#         }
#         expected_count = 1
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         self.assertEqual(len(results), 1)
#         self.assertEqual(results[0]['user'], self.user.id)
#         self.assertEqual(results[0]['post'], post.id)

#     def test_admin_user_can_filter_likes_by_user_id_regardless_of_permission(self):
#         # Arrange
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user) 
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user=self.user) 
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user) 
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user) 
#         LikeFactory.create_batch(3)
#         query_params = {
#             'user': self.user.id,
#         }
#         admin_user=CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         expected_count = 10
#         # Act
#         response = self.client.get(self.url, data=query_params)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_unauthenticated_user_only_can_list_active_public_post_likes(self):
#         # Arrange
#         self.client.logout()
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, is_active=True)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, is_active=False)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=True)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=False)
#         expected_count = 3
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')    
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             post_db = Post.objects.get(id=like['post'])
#             self.assertIs(like['is_active'], True)
#             self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)

#     def test_logged_in_user_only_can_list_active_public_and_authenticated_post_likes(self):
#         # Arrange
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, is_active=True)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, is_active=False)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=True)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=False)
#         expected_count = 6
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')    
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             self.assertIs(like['is_active'], True)

#     def test_logged_in_user_can_only_list_active_same_team_likes(self):
#         # Arrange
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=True, user=self.user, post__user__team=self.team)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=True, user__team=self.team, post__user__team=self.team)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=False, user=self.user, post__user__team=self.team)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=True)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=False)
#         expected_count = 6
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')    
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#         for like in results:
#             post_db = Post.objects.get(id=like['post'])
#             self.assertIs(like['is_active'], True)
#             self.assertEqual(post_db.read_permission, ReadPermissions.TEAM)
#             self.assertEqual(post_db.user.team.id, self.team.id)

#     def test_logged_in_user_can_only_list_active_author_team(self):
#         # Arrange
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHOR, is_active=True, user=self.user, post__user=self.user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHOR, is_active=False, user=self.user, post__user=self.user)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHOR, is_active=True)
#         LikeFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHOR, is_active=False)
#         expected_count = 3
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')    
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for like in results:
#             post_db = Post.objects.get(id=like['post'])
#             self.assertIs(like['is_active'], True)
#             self.assertEqual(post_db.read_permission, ReadPermissions.AUTHOR)
#             self.assertEqual(post_db.user.id, self.user.id)

#     def test_admin_user_can_list_active_and_inactive_likes(self):
#         # Arrange
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC, is_active=True)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC, is_active=False)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=True)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=False)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, is_active=True)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, is_active=False)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, is_active=False)
#         LikeFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, is_active=False)
#         expected_count = 16
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')    
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)


# class LikeDeleteViewTests(APITestCase):

#     def setUp(self):
#         self.team = TeamFactory()
#         self.user = CustomUserFactory(team=self.team)
#         self.post = PostFactory(user=self.user, read_permission=ReadPermissions.PUBLIC)
#         self.like = LikeFactory(user=self.user, post=self.post)
#         self.client.force_authenticate(self.user)
#         self.url = 'like-delete'


#     def test_unauthenticated_user_can_not_delete_a_active_public_like(self):
#         # Assert
#         self.client.logout()
#         url = reverse(self.url, kwargs={"user": self.user.id, "post": self.post.id})
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_a_logged_in_user_can_delete_a_like_created_by_themselves(self):
#         # Arrange
#         url = reverse(self.url, kwargs={"user": self.user.id, "post": self.post.id})
#         expected_count = 1
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         like_db_count = Like.objects.count()
#         like_db = Like.objects.filter(id=self.like.id)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertNotEqual(len(like_db), 0)
#         self.assertEqual(like_db_count, expected_count)
#         self.assertFalse(like_db[0].is_active)


#     def test_logged_in_user_can_not_delete_like_created_by_other_user(self):
#         # Arrange
#         other_user = CustomUserFactory()
#         self.client.force_authenticate(other_user)
#         url = reverse(self.url, kwargs={"user": self.user.id, "post": self.post.id})
#         expected_count = 1
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         like_db_count = Like.objects.count()
#         like_db = Like.objects.filter(id=self.like.id)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertNotEqual(len(like_db), 0)
#         self.assertEqual(like_db_count, expected_count)
#         self.assertTrue(like_db[0].is_active)


#     def test_admin_user_can_update_any_like_regardless_of_permissions(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         url = reverse(self.url, kwargs={"user": self.user.id, "post": self.post.id})
#         expected_count = 1
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         like_db_count = Like.objects.count()
#         like_db = Like.objects.filter(id=self.like.id)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertNotEqual(len(like_db), 0)
#         self.assertEqual(like_db_count, expected_count)
#         self.assertFalse(like_db[0].is_active)

#     def test_logged_in_user_can_not_delete_like_with_invalid_lookup_fields_post_invalid(self):
#         # Arrange
#         url = reverse(self.url, kwargs={"user": self.user.id, "post": (self.post.id + 1)}) # This post does not exists
#         expected_count = 1
#         like_db = Like.objects.filter(user=self.user.id, post=self.post.id+1)
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         like_db_count = Like.objects.count()
#         like_db = Like.objects.filter(id=self.like.id)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertNotEqual(len(like_db), 0)
#         self.assertEqual(like_db_count, expected_count)
#         self.assertTrue(like_db[0].is_active)

#     def test_logged_in_user_can_not_delete_like_with_invalid_lookup_fields_user_invalid(self):
#         # Arrange
#         url = reverse(self.url, kwargs={"user": self.user.id + 1, "post": (self.post.id)}) # This post does not exists
#         expected_count = 1
#         like_db = Like.objects.filter(user=self.user.id, post=self.post.id+1)
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         like_db_count = Like.objects.count()
#         like_db = Like.objects.filter(id=self.like.id)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertNotEqual(len(like_db), 0)
#         self.assertEqual(like_db_count, expected_count)
#         self.assertTrue(like_db[0].is_active)





        
        
 