import random
from django.forms.models import model_to_dict
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from post.tests.factories import PostFactory
from post.models import Post
from user.tests.factories import CustomUserFactory
from user.models import CustomUser
from team.tests.factories import TeamFactory
from like.models import Like
from like.tests.factories import LikeFactory
from comment.tests.factories import CommentFactory
from comment.models import Comment
from common.constants import READ_PERMISSIONS, ReadPermissions, EXCERPT_LENGTH
from common.paginator import TenResultsSetPagination

class PostUnauthenticatedUserViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUserFactory()
        self.data = {
            "title": "test title",
            "content": "This is the content of the Post",
            "read_permission": "public"
        }

    def test_a_unauthenticated_user_can_not_create_a_post_and_403_its_returned(self):
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

    def test_a_unauthenticated_user_can_not_edit_a_post_with_put_and_403_is_returned(self):
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

    def test_an_unauthenticated_user_can_not_edit_a_post_with_patch_and_403_is_returned(self):
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
            "content": "In the vast expanse of the digital realm, where data flows like rivers and information is the currency of the age, a new frontier emerges. This frontier is not of the physical world, but of the digital, where the boundaries between the tangible and the intangible blur. It is a place where the lines between reality and virtuality are as thin as a whisper, and where the fabric of the universe is woven from the threads of code and binary. In this realm, the heroes are not knights in shining armor, but programmers and engineers, wizards of the code, who conjure up solutions from the ether of logic and creativity. They are the architects of the digital world, building bridges between the old and the new, between the familiar and the unknown. Their tools are not swords or shields, but algorithms and frameworks, their weapons are not physical but digital, their battles are not fought with steel but with bytes.",
            "read_permission": "public"
        }
        self.url = reverse('post-list-create')
        self.client.force_authenticate(self.user)

    def test_an_authenticated_user_can_create_a_post_successfully(self):
        # Arrange
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        post_db = Post.objects.get(id=response.data.get('id'))
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), current_posts + 1)
        self.assertIsNotNone(response.data.get('id'))
        self.assertIsNotNone(response.data.get('user'))
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertNotEqual(response.data.get('id'), "")
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['content'], self.data['content'])
        self.assertEqual(response.data["excerpt"], self.data["content"][:EXCERPT_LENGTH])
        self.assertLessEqual(len(response.data["excerpt"]), EXCERPT_LENGTH)
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

    def test_create_a_post_with_no_content_should_return_400_and_the_post_is_not_created(self):
        # Arrange
        self.data['content'] = ""
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_create_a_post_without_content_should_return_400_and_the_post_is_not_created(self):
        # Arrange
        self.data.pop('content')
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)


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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
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


    def test_update_put_read_permission_by_unauthorized_user_returns_404(self):
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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
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

    def test_update_patch_read_permission_by_unauthorized_user_returns_404(self):
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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(last_modified_db, last_modified_db_after_request)
        self.assertNotEqual(Post.objects.get(id=self.post.id).read_permission, new_permission)

    def test_update_put_read_permission_with_an_invalid_permission_returns_400(self):
        # Arrange
        self.data['read_permission'] = 'invalid permission'
        last_modified_db = Post.objects.get(id=self.post.id).last_modified
        # Act
        response = self.client.put(self.url, self.data)
        # Assert
        post_db = Post.objects.get(id=self.post.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(post_db.read_permission, self.data['read_permission'])

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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
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


    def test_update_the_content_with_patch_method_and_is_admin_user_also_updates_the_excerpt(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        new_content = "This is the new content"
        self.data['content'] = new_content
        post_db = Post.objects.get(id=self.post.id)
        # Act
        response = self.client.put(self.url, self.data)
        post_db_after_request = Post.objects.get(id=self.post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(post_db.excerpt, post_db_after_request.excerpt)
        self.assertEqual(post_db_after_request.excerpt, data["content"][:EXCERPT_LENGTH])
        self.assertLessEqual(len(post_db_after_request.excerpt), EXCERPT_LENGTH)


    def test_update_the_content_with_patch_method_and_is_admin_user_also_updates_the_excerpt(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        new_content = "This is the new content"
        data = {
            "content": new_content
        }
        post_db = Post.objects.get(id=self.post.id)
        # Act
        response = self.client.patch(self.url, data)
        post_db_after_request = Post.objects.get(id=self.post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(post_db.excerpt, post_db_after_request.excerpt)
        self.assertEqual(post_db_after_request.excerpt, data["content"][:EXCERPT_LENGTH])
        self.assertLessEqual(len(post_db_after_request.excerpt), EXCERPT_LENGTH)


    def test_update_the_content_with_put_method_and_is_write_public_post_also_updates_the_excerpt(self):
        pass

    def test_update_the_content_with_put_method_and_is_write_authenticated_post_also_updates_the_excerpt(self):
        pass

    def test_update_the_content_with_put_method_and_is_write_team_post_also_updates_the_excerpt(self):
        pass

    def test_update_the_content_with_put_method_and_is_write_author_post_also_updates_the_excerpt(self):
        pass


class PostListViewTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.url = reverse('post-list-create')
        self.client.force_authenticate(self.user)
        

    def test_anonymous_user_only_can_list_public_posts(self):
        # Arrange
        self.client.logout()
        expected_count = 3
        PostFactory.create_batch(3, read_permission=ReadPermissions.PUBLIC)
        PostFactory.create_batch(3, read_permission=ReadPermissions.AUTHENTICATED)
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        self.assertLessEqual(len(results), TenResultsSetPagination.page_size)
        for post in results:
            self.assertEqual(post['read_permission'], 'public')
               

    def test_admin_user_can_list_every_post_regardless_of_the_permission(self):
        # Arrange
        PostFactory.create_batch(2, read_permission=ReadPermissions.PUBLIC)
        PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHENTICATED)
        PostFactory.create_batch(2, read_permission=ReadPermissions.TEAM)
        PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR)
        expected_count = 8
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for post in results:
            self.assertNotEqual(admin_user.id, post['user'])

    def test_logged_in_user_can_list_public_and_authenticated_posts(self):
        # Arrange
        PostFactory.create_batch(2, read_permission=ReadPermissions.PUBLIC)
        PostFactory.create_batch(3, read_permission=ReadPermissions.AUTHENTICATED)
        expected_count = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for post in results:
            self.assertNotEqual(post['read_permission'], ReadPermissions.TEAM)
            self.assertNotEqual(post['read_permission'], ReadPermissions.AUTHOR)

    def test_logged_in_user_can_list_team_posts(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        PostFactory.create_batch(2, read_permission=ReadPermissions.TEAM, user=other_user)
        PostFactory.create_batch(3, read_permission=ReadPermissions.TEAM, user=self.user)
        expected_count = 5
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for post in results:
            self.assertNotEqual(post['read_permission'], ReadPermissions.AUTHOR)

    def test_logged_in_user_can_list_same_team_posts_but_not_those_with_author_permission_by_other_user(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        PostFactory.create_batch(3, read_permission=ReadPermissions.TEAM, user=other_user)
        PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=other_user)
        expected_count = 3
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for post in results:
            self.assertNotEqual(post['read_permission'], ReadPermissions.AUTHOR)

    def test_logged_in_user_can_list_public_authenticated_team_and_self_posts(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        PostFactory.create_batch(2, read_permission=ReadPermissions.PUBLIC)
        PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHENTICATED)
        PostFactory.create_batch(2, read_permission=ReadPermissions.TEAM, user=other_user)
        PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=self.user)
        expected_count = 8
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_logged_in_user_can_list_team_and_self_posts(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        PostFactory.create_batch(1, read_permission=ReadPermissions.TEAM, user=self.user)
        PostFactory.create_batch(1, read_permission=ReadPermissions.TEAM, user=other_user)
        PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=self.user)
        expected_count = 4
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_logged_in_user_can_not_list_author_posts_by_other_user(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=self.user)
        PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=other_user)
        expected_count = 2
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_user_without_any_post_available_to_see_will_receive_empty_list(self):
        # Arrange
        user = CustomUserFactory()
        self.client.force_authenticate(user)
        PostFactory.create_batch(10, read_permission=ReadPermissions.AUTHOR)
        expected_count = 0
        #  Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        self.assertLessEqual(len(results), expected_count)
       
class PostRetrieveViewTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)

    def test_anonymous_user_can_retrieve_a_public_post(self):
        # Arrange
        self.client.logout()
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

    def test_anonymous_user_can_not_retrieve_an_authenticated_post(self):
        # Arrange
        self.client.logout()
        post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_user_can_not_retrieve_a_team_post(self):
        # Arrange
        self.client.logout()
        post = PostFactory(read_permission=ReadPermissions.TEAM)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_anonymous_user_can_not_retrieve_an_author_post(self):
        # Arrange
        self.client.logout()
        post = PostFactory(read_permission=ReadPermissions.AUTHOR)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_retrieve_a_public_post(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

    def test_logged_in_user_can_retrieve_an_authenticated_post(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

    def test_logged_in_user_can_retrieve_a_team_post_when_the_user_is_in_the_same_team(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

    def test_logged_in_user_can_not_retrieve_a_team_post_if_the_user_does_not_belong_to_that_team(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_retrieve_an_author_post_when_the_user_wrote_it(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=self.user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

    def test_logged_in_user_can_not_retrieve_an_author_post_when_the_user_does_not_wrote_it(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=other_user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_retrieve_a_public_post_if_was_written_by_themselves(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.PUBLIC, user=self.user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

    def test_logged_in_user_can_retrieve_an_authenticated_post_if_was_written_by_themselves(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

    def test_logged_in_user_can_retrieve_a_team_post_if_was_written_by_themselves(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=self.user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)        
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)


    def test_admin_user_can_retrieve_a_public_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)        
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

    def test_admin_user_can_retrieve_an_authenticated_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)        
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)
        

    def test_admin_user_can_retrieve_a_team_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=self.user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)        
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)
        

    def test_admin_user_can_retrieve_an_author_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=self.user)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act & Assert
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('user'), post.user.id)
        self.assertEqual(response.data.get('read_permission'), post.read_permission)
        self.assertEqual(response.data.get('id'), post.id)
        self.assertEqual(response.data.get('title'), post.title)
        self.assertEqual(response.data.get('content'), post.content)        
        self.assertEqual(response.data.get('excerpt'), post.excerpt)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

class PostDeleteViewTests(APITestCase):
    
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.post = PostFactory(user=self.user, read_permission=ReadPermissions.PUBLIC)
        self.url = "post-retrieve-update-delete"
        self.client.force_authenticate(self.user)

    def test_unauthenticated_user_can_not_delete_posts(self):
        # Arrange
        self.client.logout()
        url = reverse(self.url, kwargs={"pk": self.post.id})
        expected_count = 1
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), expected_count)

    def test_logged_in_user_can_not_delete_a_post_that_does_not_belong_to_themselves(self):
        # Arrange
        other_user = CustomUserFactory()
        self.client.force_authenticate(other_user)
        url = reverse(self.url, kwargs={"pk": self.post.id})
        expected_count = 1
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), expected_count)

    def test_logged_in_user_can_delete_a_post_that_belong_to_themselves(self):
        # Arrange
        url = reverse(self.url, kwargs={"pk": self.post.id})
        expected_count = 0
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), expected_count)

    def test_logged_in_user_delete_a_post_and_likes_and_comments_are_also_destroyed(self):
        # Arrange
        LikeFactory.create_batch(2, post=self.post)
        CommentFactory.create_batch(2, post=self.post)
        url = reverse(self.url, kwargs={"pk": self.post.id})
        expected_count = 0
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), expected_count)
        self.assertEqual(Comment.objects.count(), expected_count)
        self.assertEqual(Like.objects.count(), expected_count)

    def test_admin_user_can_delete_any_post_regardless_of_permission(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        LikeFactory.create_batch(2, post=self.post)
        CommentFactory.create_batch(2, post=self.post)
        url = reverse(self.url, kwargs={"pk": self.post.id})
        expected_count = 0
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), expected_count)
        self.assertEqual(Comment.objects.count(), expected_count)
        self.assertEqual(Like.objects.count(), expected_count)

    def test_logged_in_user_try_to_delete_a_non_existing_post_and_404_is_returned(self):
        # Arrange
        post = Post.objects.get(id=self.post.id)
        post.delete()
        url = reverse(self.url, kwargs={"pk": self.post.id})
        expected_count = 0
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), expected_count)




