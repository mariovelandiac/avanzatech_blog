from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from like.models import Like
from user.tests.factories import CustomUserFactory
from post.tests.factories import PostFactory
from post.constants import ReadPermissions
from team.tests.factories import TeamFactory
from common.constants import Status

class LikeCreateViewTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.post = PostFactory(user=self.user)
        self.client.force_authenticate(self.user)
        self.data = {
            "post": self.post.id,
            "user": self.user.id
        }
        self.url = reverse('like-list-create')
    
    def test_unauthenticated_user_can_not_create_a_like(self):
        # Arrange
        self.client.logout()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_create_a_like_in_a_post_created_by_themselves_regardless_of_permission(self):
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id)
        self.assertEqual(response.data.get('post'), self.post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)

    def test_logged_in_user_can_not_create_more_than_one_like_to_one_post(self):
        # Act
        response = self.client.post(self.url, self.data)
        response = self.client.post(self.url, self.data)
        expected_likes_db = 1
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_create_a_like_in_a_public_post(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
        self.data['post'] = post.id
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id) # Created by the authenticated user
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)

    def test_logged_in_user_can_create_a_like_in_an_authenticated_post(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
        self.data['post'] = post.id
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id) # Created by the authenticated user
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
    
    def test_logged_in_user_can_create_a_like_in_a_team_post_if_belongs_to_same_team(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id) # Created by the authenticated user
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_not_create_a_like_a_in_a_team_post_if_does_not_belongs_to_that_team(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
        self.data['post'] = post.id
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_not_create_a_like_in_a_author_post_that_does_not_belong_themselves(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=other_user)
        self.data['post'] = post.id
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_logged_in_user_can_create_a_like_in_a_author_post_that_belongs_themselves(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=self.user)
        self.data['post'] = post.id
        expected_likes_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_a_logged_in_user_can_not_create_a_like_in_a_post_that_does_not_exist(self):
        # Arrange
        self.data['post'] = self.post.id + 1 # this post doesn't exist
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_invalid_data_returns_a_404_status_code(self):
        # Arrange
        data = {
                "post_id": self.post.id,
                "user_id": self.user.id
                }
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_admin_user_can_create_a_like_in_public_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
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

    def test_admin_user_can_create_a_like_in_an_authenticated_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
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

    def test_admin_user_can_create_a_like_in_a_team_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.TEAM)
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
    
    def test_admin_user_can_create_a_like_in_an_author_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.AUTHOR)
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
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
        self.data['user'] = other_user.id
        self.data['post'] = post.id
        expected_likes_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), expected_likes_db)

    def test_a_logged_in_user_can_change_a_like_from_inactive_to_active(self):
        # Arrange
        like = Like.objects.create(user=self.user, post=self.post, is_active=False)
        expected_likes_db = 1
        print("this is the like status", like.is_active)
        # Act
        response = self.client.post(self.url, self.data)
        total_likes = Like.objects.count()
        # Assert
        like_db = Like.objects.get(id=like.id)
        print(list(Like.objects.all().values()))
        print("this is the like status", like_db.is_active)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(total_likes, expected_likes_db)
        self.assertEqual(response.data['is_active'], like_db.is_active)
        self.assertIs(response.data['is_active'], True)

class LikeListViewTests(APITestCase):

    pass










        
        
