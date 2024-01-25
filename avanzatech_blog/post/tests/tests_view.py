from django.forms.models import model_to_dict
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from user.tests.factories import CustomUserFactory
from post.tests.factories import PostFactory
from post.models import Post
from user.models import CustomUser

class PostUnauthenticatedUserViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUserFactory()
        self.data = {
            "title": "test_title",
            "content": "This is the content of the Post",
            "user": self.user.id,
            "read_permission": "public"
        }
        self.url = reverse('post-list-create')

    def test_an_unauthenticated_user_can_not_create_a_post_and_403_its_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        expected_response = "not_authenticated"
        # Act
        response = self.client.post(self.url, self.data)
        auth_response = response.data.get('detail').code
        # Assert
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(auth_response, expected_response)
        self.assertEqual(Post.objects.count(), current_posts)

class PostAuthenticatedUserViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUserFactory()
        self.data = {
            "title": "test_title",
            "content": "This is the content of the Post",
            "user": self.user.id,
            "read_permission": "public"
        }
        self.url = reverse('post-list-create')
        self.client.force_authenticate(self.user)

    def test_an_authenticated_user_can_create_a_post_successfully(self):
        # Arrange
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), current_posts + 1)
        self.assertIsNotNone(response.data.get('id'))
        self.assertNotEqual(response.data.get('id'), "")
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['content'], self.data['content'])
        self.assertEqual(response.data['user'], self.data['user'])
        self.assertEqual(response.data['read_permission'], self.data['read_permission'])

    def test_create_a_post_with_no_title_should_return_400(self):
        # Arrange
        self.data['title'] = ""
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_create_a_post_without_title_should_return_400(self):
        # Arrange
        self.data.pop('title')
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_create_a_post_with_no_content_should_return_201_and_the_post_is_created(self):
        # Arrange
        self.data['content'] = ""
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), current_posts + 1)

    def test_create_a_post_without_content_should_return_201_and_the_post_is_created(self):
        # Arrange
        self.data.pop('content')
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), current_posts + 1)


    def test_create_a_post_without_read_permission_should_return_400(self):
        # Arrange
        self.data.pop('read_permission')
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_create_a_post_with_an_invalid_read_permission_should_return_400(self):
        # Arrange
        self.data['read_permission'] = "invalid permission"
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_create_a_post_without_associated_user_should_return_400(self):
        # Arrange
        self.data.pop('user')
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_create_a_post_with_an_invalid_user_should_return_400(self):
        # Arrange
        self.data['user'] = self.data['user'] + 1 # This user doesn't exist
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)








