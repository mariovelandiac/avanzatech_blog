from django.forms.models import model_to_dict
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from user.tests.factories import CustomUserFactory
from post.tests.factories import PostFactory
from post.models import Post
from post.constants import READ_PERMISSIONS
from user.models import CustomUser

class PostUnauthenticatedUserViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUserFactory()
        self.data = {
            "title": "test title",
            "content": "This is the content of the Post",
            "read_permission": "public"
        }

    def test_an_unauthenticated_user_can_not_create_a_post_and_403_its_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        expected_response = "not_authenticated"
        # Act
        url = reverse('post-list-create')
        response = self.client.post(url, self.data)
        auth_response = response.data.get('detail').code
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(auth_response, expected_response)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_an_authenticated_user_can_not_edit_a_post_with_put_and_403_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        current_posts = Post.objects.count()
        expected_response = "not_authenticated"
        url = reverse('post-retrieve-update-delete', args=[post.id])
        self.data['title'] = "new title"
        # Act
        response = self.client.put(url, self.data)
        auth_response = response.data.get('detail').code
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(auth_response, expected_response)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_an_authenticated_user_can_not_edit_a_post_with_patch_and_403_is_returned(self):
        # Arrange
        post = PostFactory(user=self.user)
        current_posts = Post.objects.count()
        expected_response = "not_authenticated"
        data = {
            "id": post.id,
            "title": "new_title"
        }
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.patch(url, data)
        auth_response = response.data.get('detail').code
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(auth_response, expected_response)
        self.assertEqual(Post.objects.count(), current_posts)

class PostCreateViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUserFactory()
        self.data = {
            "title": "test_title",
            "content": "This is the content of the Post",
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
        self.assertIsNotNone(response.data.get('user'))
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertNotEqual(response.data.get('id'), "")
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['content'], self.data['content'])
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

    def test_create_a_post_sets_automatically_user_id_from_the_request(self):
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.data.get('user'), self.user.id)

class PostUpdateViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUserFactory()
        self.post = PostFactory(user=self.user)
        self.data = {
            "title": self.post.title,
            "content": self.post.content,
            "read_permission": self.post.read_permission
        }
        self.url = reverse('post-retrieve-update-delete', args=[self.post.id])
        self.client.force_authenticate(self.user)

    def test_update_the_title_with_put_method_is_allowed_for_owner_of_the_post(self):
        # Arrange
        new_title = "this is a new title"
        self.data['title'] = new_title
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).title, new_title)
        self.assertEqual(self.post.id, response.data.get('id'))


    def test_update_the_title_with_patch_method_is_allowed_for_owner_of_the_post(self):
        # Arrange
        new_title = "this is a new title"
        data = {
            "title": new_title
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).title, new_title)
    

    def test_update_the_title_with_put_method_is_forbidden_for_another_user_from_the_request_user(self):
        # Arrange
        another_user = CustomUserFactory()
        self.client.force_authenticate(another_user)
        new_title = "this is a new title"
        self.data['title'] = new_title
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(last_modified_db, last_modified_db_after_request)
        self.assertNotEqual(Post.objects.get(id=self.post.id).title, new_title)

    def test_update_the_title_with_patch_method_is_forbidden_for_another_user_from_the_request_user(self):
        # Arrange
        another_user = CustomUserFactory()
        self.client.force_authenticate(another_user)
        new_title = "this is a new title"
        data = {
            "title": new_title
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(last_modified_db, last_modified_db_after_request)
        self.assertNotEqual(Post.objects.get(id=self.post.id).title, new_title)

    def test_update_the_title_with_put_method_and_is_admin_user_is_carried_out_successfully(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        new_title = "this is a new title"
        self.data['title'] = new_title
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).title, new_title)

    def test_update_the_title_with_patch_method_and_is_admin_user_is_carried_out_successfully(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        new_title = "this is a new title"
        data = {
            "title": new_title
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).title, new_title)

    def test_update_put_read_permission_is_carried_out_successfully(self):
        # Arrange
        for permission in list(READ_PERMISSIONS.keys()):
            if permission != self.post.read_permission:
                self.data['read_permission'] = permission
                break
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).read_permission, self.data['read_permission'])


    def test_update_put_read_permission_by_unauthorized_user_returns_403(self):
        # Arrange
        another_user = CustomUserFactory()
        self.client.force_authenticate(another_user)
        for permission in list(READ_PERMISSIONS.keys()):
            if permission != self.post.read_permission:
                self.data['read_permission'] = permission
                break
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(last_modified_db, last_modified_db_after_request)
        self.assertNotEqual(Post.objects.get(id=self.post.id).read_permission, self.data['read_permission'])

    def test_update_put_read_permission_by_admin_is_carried_out_successfully(self):
        # Arrange
        another_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(another_user)
        for permission in list(READ_PERMISSIONS.keys()):
            if permission != self.post.read_permission:
                self.data['read_permission'] = permission
                break
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).read_permission, self.data['read_permission'])

    def test_update_patch_read_permission_is_carried_out_successfully(self):
        # Arrange
        new_permission = None
        for permission in list(READ_PERMISSIONS.keys()):
            if permission != self.post.read_permission:
                new_permission = permission
                break
        data = {
            "read_permission": new_permission
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).read_permission, new_permission)

    def test_update_patch_read_permission_by_unauthorized_user_returns_403(self):
        # Arrange
        another_user = CustomUserFactory()
        self.client.force_authenticate(another_user)
        new_permission = None
        for permission in list(READ_PERMISSIONS.keys()):
            if permission != self.post.read_permission:
                new_permission = permission
                break
        data = {
            "read_permission": new_permission
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(last_modified_db, last_modified_db_after_request)
        self.assertNotEqual(Post.objects.get(id=self.post.id).read_permission, new_permission)

    def test_update_patch_read_permission_by_admin_is_carried_out_successfully(self):
        # Arrange
        another_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(another_user)
        new_permission = None
        for permission in list(READ_PERMISSIONS.keys()):
            if permission != self.post.read_permission:
                new_permission = permission
                break
        data = {
            "read_permission": new_permission
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).read_permission, new_permission)

    def test_update_the_content_with_patch_method_is_allowed_for_owner_of_the_post(self):
        # Arrange
        new_content = "This is the new content"
        self.data['content'] = new_content
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).content, new_content)


    def test_update_the_content_with_patch_method_is_allowed_for_owner_of_the_post(self):
        # Arrange
        new_content = "This is the new content"
        data = {
            "content": new_content
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).content, new_content)
    

    def test_update_the_content_with_put_method_is_forbidden_for_another_user_from_the_request_user(self):
        # Arrange
        another_user = CustomUserFactory()
        self.client.force_authenticate(another_user)
        new_content = "This is the new content"
        self.data['content'] = new_content
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(last_modified_db, last_modified_db_after_request)
        self.assertNotEqual(Post.objects.get(id=self.post.id).content, new_content)

    def test_update_the_content_with_patch_method_is_forbidden_for_another_user_from_the_request_user(self):
        # Arrange
        another_user = CustomUserFactory()
        self.client.force_authenticate(another_user)
        new_content = "This is the new content"
        data = {
            "content": new_content
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(last_modified_db, last_modified_db_after_request)
        self.assertNotEqual(Post.objects.get(id=self.post.id).content, new_content)

    def test_update_the_content_with_put_method_and_is_admin_user_is_carried_out_successfully(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        new_content = "This is the new content"
        self.data['content'] = new_content
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).content, new_content)

    def test_update_the_content_with_patch_method_and_is_admin_user_is_carried_out_successfully(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        new_content = "This is the new content"
        data = {
            "content": new_content
        }
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.patch(self.url, data)
        # Assert
        last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(last_modified_db, last_modified_db_after_request)
        self.assertEqual(Post.objects.get(id=self.post.id).content, new_content)