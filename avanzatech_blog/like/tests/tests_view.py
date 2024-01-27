from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
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
            "post": self.post.id
        }
        self.url = reverse('like-list-create')
    
    def test_unauthenticated_user_can_not_create_a_like(self):
        # Arrange
        self.client.logout()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_create_a_like_in_a_post_created_by_themselves(self):
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id)
        self.assertEqual(response.data.get('post'), self.post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('status'), Status.ACTIVE)

    def test_logged_in_user_can_create_a_like_in_a_public_post(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
        data = {"post": post.id}
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id) # Created by the authenticated user
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('status'), Status.ACTIVE)

    def test_logged_in_user_can_create_a_like_in_an_authenticated_post(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
        data = {"post": post.id}
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id) # Created by the authenticated user
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('status'), Status.ACTIVE)
    
    def test_logged_in_user_can_create_a_like_in_a_team_post_if_belongs_to_same_team(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
        data = {"post": post.id}
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id) # Created by the authenticated user
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('status'), Status.ACTIVE)






        
        
