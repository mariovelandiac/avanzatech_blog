from django.forms.models import model_to_dict
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from post.tests.factories import PostFactory, PostCategoryPermissionFactory
from post.models import Post, PostCategoryPermission
from user.tests.factories import CustomUserFactory
from user.models import CustomUser
from team.tests.factories import TeamFactory
from like.models import Like
from like.tests.factories import LikeFactory
from comment.tests.factories import CommentFactory
from comment.models import Comment
from category.tests.factories import CategoryFactory
from permission.tests.factories import PermissionFactory
from common.constants import EXCERPT_LENGTH, CONTENT_MOCK, CATEGORIES, AccessCategory, AccessPermission
from common.paginator import TenResultsSetPagination
from common.utils import create_custom_category_permissions_handler, create_default_category_permissions_handler

class PostUnauthenticatedUserCreateViewTests(APITestCase):

    def test_an_unauthenticated_user_can_not_create_a_post_and_a_403_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        expected_response = "not_authenticated"
        categories = CategoryFactory.create_batch()
        permissions = PermissionFactory.create_batch()
        data = {
            "title": "test title",
            "content": "This is the content of the Post",
            "category_permission": create_default_category_permissions_handler(categories, permissions)
        }
        # Act
        url = reverse('post-list-create')
        response = self.client.post(url, data, format='json')
        auth_response = response.data.get('detail').code
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(auth_response, expected_response)
        self.assertEqual(Post.objects.count(), current_posts)

class PostUnauthenticatedUserListViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('post-list-create')
        CategoryFactory.create_batch()
        PermissionFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }

    
    def test_unauthenticated_user_can_see_public_posts_when_posts_have_public_read_permission(self):
        # Arrange
        amount_posts = 4
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        posts = PostFactory.create_batch(amount_posts)
        post_category_permission = PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(amount_posts, count)
        self.assertEqual(len(results), amount_posts)

    def test_unauthenticated_user_can_see_public_posts_when_posts_have_public_edit_permission(self):
        # Arrange
        amount_posts = 4
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        posts = PostFactory.create_batch(amount_posts)
        post_category_permission = PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(amount_posts, count)
        self.assertEqual(len(results), amount_posts)


    def test_unauthenticated_user_can_not_list_public_post_when_post_have_not_public_permission(self):
        # Arrange
        no_permission_public_posts = 2
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        posts_no_permission = PostFactory.create_batch(no_permission_public_posts)
        post_category_permission = PostCategoryPermissionFactory.create_batch(posts_no_permission, category_permission=self.factory_category_permission)
        read_public_posts = 2
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        posts_read = PostFactory.create_batch(read_public_posts)
        post_category_permission = PostCategoryPermissionFactory.create_batch(posts_read, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), read_public_posts)
        self.assertEqual(len(response.data.get('results')), read_public_posts)
        
class PostUnauthenticatedUserRetrieveViewTests(APITestCase):

    def setUp(self):
        CategoryFactory.create_batch()
        PermissionFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }

    def test_unauthenticated_user_receive_user_first_and_last_name_when_retrieve_public_posts(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('user').get('first_name'), post.user.first_name)
        self.assertEqual(data.get('user').get('last_name'), post.user.last_name)

    def test_unauthenticated_user_does_not_receive_excerpt_when_see_post_details(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('excerpt', data)

    def test_unauthenticated_user_can_not_see_post_details_when_post_has_not_public_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_can_see_post_details_when_post_has_public_read_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_unauthenticated_user_can_see_post_details_when_post_has_public_edit_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

class PostUnauthenticatedUserEditViewTests(APITestCase):

    def setUp(self):
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }
        self.categories = CategoryFactory.create_batch()
        self.permissions = PermissionFactory.create_batch()
        self.category_permissions = create_default_category_permissions_handler(self.categories, self.permissions)
        self.data = {
            "title": "test title",
            "content": "This is the content of the Post",
            "category_permission": self.category_permissions
        }
    

    def test_unauthenticated_user_can_edit_with_patch_title_of_a_post_with_public_edit_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        new_title = "new title"
        data = {
            "title": new_title
        }
        # Act
        response = self.client.patch(url, data, format='json')
        # Assert
        post_db = Post.objects.get(id=post.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), new_title)
        self.assertEqual(post_db.title, data["title"])

    def test_unauthenticated_user_can_edit_with_patch_content_of_a_post_with_public_edit_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        new_content = "new content"
        data = {
            "content": new_content
        }
        # Act
        response = self.client.patch(url, data, format='json')
        # Assert
        post_db = Post.objects.get(id=post.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('content'), new_content)
        self.assertEqual(post_db.content, data["content"])

    def test_unauthenticated_user_can_not_edit_with_patch_title_of_a_post_with_public_read_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        new_title = "new title"
        data = {
            "title": new_title
        }
        # Act
        response = self.client.patch(url, data, format='json')
        # Assert
        post_db = Post.objects.get(id=post.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.data.get('title'), new_title)
        self.assertNotEqual(post_db.title, data["title"])

    def test_unauthenticated_user_can_not_edit_with_patch_content_of_a_post_with_public_read_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        new_content = "new content"
        data = {
            "content": new_content
        }
        # Act
        response = self.client.patch(url, data, format='json')
        # Assert
        post_db = Post.objects.get(id=post.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.data.get('content'), new_content)
        self.assertNotEqual(post_db.content, data["content"])

    def test_unauthenticated_user_can_not_edit_with_patch_title_of_a_post_with_no_permissions_at_all(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        new_title = "new title"
        data = {
            "title": new_title
        }
        # Act
        response = self.client.patch(url, data, format='json')
        # Assert
        post_db = Post.objects.get(id=post.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.data.get('title'), new_title)
        self.assertNotEqual(post_db.title, data["title"])

    def test_unauthenticated_user_can_not_edit_with_patch_content_of_a_post_with_permissions_at_all(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        new_content = "new content"
        data = {
            "content": new_content
        }
        # Act
        response = self.client.patch(url, data, format='json')
        # Assert
        post_db = Post.objects.get(id=post.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.data.get('content'), new_content)
        self.assertNotEqual(post_db.content, data["content"])

    def test_an_unauthenticated_user_with_edit_permission_can_edit_a_public_post_with_put_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        post_after_updating = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_after_updating.title, self.data['title'])

    def test_an_unauthenticated_user_without_edit_permission_can_not_edit_a_post_with_put_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        post_after_updating = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(post_after_updating.title, self.data['title'])

    def test_an_unauthenticated_user_without_any_permission_can_not_edit_a_post_with_put_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        post_after_updating = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(post_after_updating.title, self.data['title'])

    def test_an_unauthenticated_user_with_edit_permission_can_edit_post_permissions_with_patch_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        permission_before_updating = post_category_permission[0].permission
        # Change public permission to read
        self.data['category_permission'] = [
            {
                "category": self.categories[0].id, #public category is in position 0
                "permission": self.permissions[0].id #read permission is in position 0
            }
        ]
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.patch(url, self.data, format='json')
        permissions_after_updating = PostCategoryPermission.objects.get(post=post, category__name=self.categories[0].name)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(permissions_after_updating.permission, self.permissions[0])
        self.assertNotEqual(permissions_after_updating.permission, permission_before_updating)
        self.assertEqual(permission_before_updating.name, AccessPermission.EDIT)

    def test_an_unauthenticated_user_with_edit_permission_can_edit_post_permissions_with_put_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        permission_before_updating = post_category_permission[0].permission
        # Change public permission to read
        self.data['category_permission'] = [
            {
                "category": self.categories[0].id, #public category is in position 0
                "permission": self.permissions[0].id #read permission is in position 0
            },
        ]
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        permissions_after_updating = PostCategoryPermission.objects.get(post=post, category__name=self.categories[0].name)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(permissions_after_updating.permission, self.permissions[0])
        self.assertNotEqual(permissions_after_updating.permission, permission_before_updating)
        self.assertEqual(permission_before_updating.name, AccessPermission.EDIT)
    
    def test_an_unauthenticated_user_can_not_edit_post_permission_with_invalid_permission_id_with_patch_and_400_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        category_position = 2
        invalid_permission = self.permissions[1].id + 200
        self.data['category_permission'] = [
            {
                "category": self.categories[category_position].id,
                "permission": invalid_permission
            }
        ]
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.patch(url, self.data, format='json')
        permissions_after_updating = PostCategoryPermission.objects.get(post=post, category__name=self.categories[category_position].name)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(permissions_after_updating.permission.id, invalid_permission)

    
    def test_an_unauthenticated_user_can_not_edit_post_permission_with_invalid_permission_id_with_put_and_400_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        category_position = 2
        invalid_permission = self.permissions[1].id + 200
        self.data['category_permission'] = [
            {
                "category": self.categories[category_position].id,
                "permission": invalid_permission
            }
        ]
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        permissions_after_updating = PostCategoryPermission.objects.get(post=post, category__name=self.categories[category_position].name)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(permissions_after_updating.permission.id, invalid_permission)

    def test_an_unauthenticated_user_without_permissions_can_not_edit_post_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        category_position = 2
        self.data['category_permission'] = [
            {
                "category": self.categories[category_position].id,
                "permission": self.permissions[1].id
            }
        ]
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        permissions_after_updating = PostCategoryPermission.objects.get(post=post, category__name=self.categories[category_position].name)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(permissions_after_updating.id, self.permissions[1].id)


    def test_an_unauthenticated_user_with_read_permissions_can_not_edit_post_permission(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        category_position = 2
        self.data['category_permission'] = [
            {
                "category": self.categories[category_position].id,
                "permission": self.permissions[1].id
            }
        ]
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        permissions_after_updating = PostCategoryPermission.objects.get(post=post, category__name=self.categories[category_position].name)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(permissions_after_updating.id, self.permissions[1].id)

    def test_an_unauthenticated_user_with_edit_permission_can_edit_several_post_permissions_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        expected_permissions = 4
        public_permission_before_updating = post_category_permission[0].permission
        authenticated_permission_before_updating = post_category_permission[1].permission
        # Change public permission to read and authenticated permission to edit
        self.data['category_permission'] = [
            {
                "category": self.categories[0].id, #public category is in position 0
                "permission": self.permissions[0].id #read permission is in position 0
            },
            {
                "category": self.categories[1].id, #authenticated category is in position 1
                "permission": self.permissions[1].id # edit permission is in position 0
            }
        ]
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        public_permission_after_updating = PostCategoryPermission.objects.get(post=post, category__name=AccessCategory.PUBLIC)
        authenticated_permission_after_updating = PostCategoryPermission.objects.get(post=post, category__name=AccessCategory.AUTHENTICATED)
        permissions_after_updating = PostCategoryPermission.objects.filter(post=post)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(public_permission_after_updating.permission, self.permissions[0])
        self.assertEqual(authenticated_permission_after_updating.permission, self.permissions[1])
        self.assertNotEqual(public_permission_after_updating.permission, public_permission_before_updating)
        self.assertNotEqual(authenticated_permission_after_updating.permission, authenticated_permission_before_updating)
        self.assertEqual(permissions_after_updating.count(), expected_permissions)
        


    def test_an_unauthenticated_user_with_edit_permission_can_edit_post_permissions_and_the_remaining_permission_does_not_change(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        expected_permissions = 4
        # Change public permission to read
        self.data['category_permission'] = [
            {
                "category": self.categories[0].id, #public category is in position 0
                "permission": self.permissions[0].id #read permission is in position 0
            }
        ]
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.put(url, self.data, format='json')
        permissions_after_updating = PostCategoryPermission.objects.filter(post=post)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(permissions_after_updating.count(), expected_permissions)
        self.assertEqual(permissions_after_updating[0].permission, self.permissions[0])
    
class PostUnauthenticatedUserDeleteViewTests(APITestCase):
    
    def setUp(self):
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }
        self.categories = CategoryFactory.create_batch()
        self.permissions = PermissionFactory.create_batch()

    def test_unauthenticated_user_can_delete_a_post_with_public_edit_permissions(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        current_posts = Post.objects.count()
        expected_permissions = 0
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url)
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), current_posts - 1)
        self.assertEqual(post_category_permission_db.count(), expected_permissions)

    def test_unauthenticated_user_can_not_delete_a_post_with_public_read_permissions(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        current_posts = Post.objects.count()
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_unauthenticated_user_can_not_delete_a_post_with_any_permission_at_all(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        current_posts = Post.objects.count()
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)
        
class PostAuthenticatedUserCreateViewTests(APITestCase):
    
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.url = reverse('post-list-create')
        self.permissions = PermissionFactory.create_batch()
        self.categories = CategoryFactory.create_batch()
        self.category_permission = create_default_category_permissions_handler(self.categories, self.permissions)
        self.data = {
            "title": "test title",
            "content": CONTENT_MOCK,
            "category_permission": self.category_permission,
        }

    def test_authenticated_user_can_create_a_post_and_201_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        post_category_permission = PostCategoryPermission.objects.filter(post=response.data.get('id'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), current_posts + 1)
        self.assertEqual(post_category_permission.count(), len(self.category_permission))

    def test_authenticated_user_can_create_a_post_and_the_user_id_is_set_automatically(self):
        # Arrange
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), current_posts + 1)
        self.assertEqual(response.data.get('user').get('id'), self.user.id)

    def test_authenticated_user_can_create_a_post_and_the_excerpt_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), current_posts + 1)
        self.assertIn('excerpt', response.data)

    def test_authenticated_user_can_create_a_post_and_the_excerpt_is_returned_with_the_correct_length(self):
        # Arrange
        current_posts = Post.objects.count()
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), current_posts + 1)
        self.assertIn('excerpt', response.data)
        self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)
        self.assertEqual(response.data.get('excerpt'), self.data.get('content')[:EXCERPT_LENGTH])

    def test_authenticated_user_can_not_create_a_post_without_title_and_a_400_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        self.data.pop('title')
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_authenticated_user_can_not_create_a_post_without_content_and_a_400_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        self.data.pop('content')
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_authenticated_user_can_not_create_a_post_without_category_permission_and_a_400_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        self.data.pop('category_permission')
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_authenticated_user_can_not_create_a_post_with_incomplete_category_permission_and_a_400_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        self.data['category_permission'] = [
            {
                "category": self.categories[0].id,
                "permission": self.permissions[0].id
            }
        ]
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_authenticated_user_can_not_create_a_post_with_invalid_category_in_category_permission_and_400_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        self.data['category_permission'][0] = {
                "category": self.categories[0].id + 200,
                "permission": self.permissions[0].id
        }
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_authenticated_user_can_not_create_a_post_with_invalid_permission_in_category_permission_and_400_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        self.data['category_permission'][0] = {
                "category": self.categories[0].id,
                "permission": self.permissions[0].id + 200
        }
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_authenticated_user_can_not_create_post_with_repeated_categories_in_payload_and_400_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        self.data['category_permission'] = [
            {
                "category": self.categories[0].id,
                "permission": self.permissions[0].id
            },
            {
                "category": self.categories[0].id,
                "permission": self.permissions[1].id
            },
            {
                "category": self.categories[1].id,
                "permission": self.permissions[1].id
            },
            {
                "category": self.categories[1].id,
                "permission": self.permissions[1].id
            }
        ]
        # Act
        response = self.client.post(self.url, self.data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), current_posts)


class PostAuthenticatedUserListViewTests(APITestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.permissions = PermissionFactory.create_batch()
        self.categories = CategoryFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }
        self.url = reverse('post-list-create')

    def test_authenticated_user_can_lists_public_or_authenticated_posts_with_read_permission_and_200_is_returned(self):
        # Arrange
        public_posts = 4
        posts = PostFactory.create_batch(public_posts)
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, public_posts)
        
    def test_authenticated_user_can_not_list_public_and_authenticated_posts_with_no_permissions_and_200_is_returned(self):
        # Arrange
        public_posts = 4
        posts = PostFactory.create_batch(public_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 0)
        self.assertEqual(len(results), 0)

    def test_authenticated_user_can_list_authenticated_posts_without_public_permission_and_200_is_returned(self):
        # Arrange
        authenticated_posts = 4
        posts = PostFactory.create_batch(authenticated_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, authenticated_posts)
        self.assertEqual(len(results), authenticated_posts)

    def test_authenticated_user_can_not_list_authenticated_posts_with_no_permissions_and_200_is_returned(self):
        # Arrange
        authenticated_posts = 4
        posts = PostFactory.create_batch(authenticated_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION    
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        expected_list_post = 0
        # Act 
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_list_post)
        self.assertEqual(len(results), expected_list_post)

    def authenticated_user_can_list_posts_with_edit_permission_and_without_public_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_authenticated_user_can_list_posts_with_public_read_permission_but_without_authenticated_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_authenticated_user_can_list_posts_with_public_edit_permission_but_without_authenticated_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_authenticated_user_can_list_posts_with_public_read_permission_but_without_team_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)
    
    def test_authenticated_user_can_list_posts_with_public_edit_permission_but_without_team_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_authenticated_user_can_list_posts_with_authenticated_read_permission_but_without_team_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)
    
    def test_authenticated_user_can_list_posts_with_public_edit_permission_but_without_author_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_authenticated_user_can_list_posts_with_read_permission_from_same_team_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts, user=self.user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_authenticated_user_can_list_posts_with_edit_permission_from_same_team_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts, user=self.user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_another_authenticated_user_can_not_list_posts_with_team_read_permission_but_from_different_team(self):
        # Arrange
        another_user = CustomUserFactory()
        self.client.force_authenticate(another_user)
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts, user=self.user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 0)

    def test_authenticated_user_can_list_posts_created_by_them_with_author_read_permission(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts, user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_authenticated_user_can_list_posts_created_by_them_with_author_edit_permission(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts, user=self.user)
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)
    
    def test_authenticated_user_can_not_list_posts_from_another_author_with_just_author_read_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 0)

    def test_authenticated_user_can_not_list_posts_from_another_author_with_just_author_edit_permission_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        results = response.data.get('results')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 0)
    
    def test_authenticated_user_can_not_list_posts_with_no_permissions_and_200_is_returned(self):
        # Arrange
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 0)

    def test_another_authenticated_user_can_list_posts_with_read_permission_from_the_same_team_and_200_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts, user=self.user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

    def test_another_authenticated_user_can_list_posts_with_edit_permission_and_200_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        amount_posts = 4
        posts = PostFactory.create_batch(amount_posts, user=self.user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        # Act
        response = self.client.get(self.url)
        # Assert
        count = response.data.get('count')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, amount_posts)

class PostAuthenticatedUserRetrieveViewTests(APITestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.permissions = PermissionFactory.create_batch()
        self.categories = CategoryFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }

    def test_authenticated_user_can_retrieve_a_post_with_public_read_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)
    
    def test_authenticated_user_can_retrieve_a_post_with_public_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_authenticated_user_can_retrieve_a_post_with_authenticated_read_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_authenticated_user_can_retrieve_a_post_with_authenticated_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_authenticated_user_can_retrieve_a_post_with_public_read_permission_but_without_authenitcated_permision_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)
    
    def test_authenticated_user_can_retrieve_a_post_with_public_edit_permission_but_without_authenticated_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_authenticated_user_can_retrieve_a_post_without_public_permission_but_with_authenticated_read_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_authenticated_user_can_retrieve_a_post_without_public_permission_but_with_authenticated_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_authenticated_user_can_not_retrieve_a_post_without_any_public_and_authenticated_post_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_another_authenticated_user_can_retrieve_post_from_the_same_team_with_read_permission_and_200_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        post = PostFactory(user=self.user)
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_another_authenticated_user_can_retrieve_post_from_the_same_team_with_edit_permission_and_200_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        post = PostFactory(user=self.user)
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_another_authenticated_user_can_not_retrieve_post_from_the_same_team_without_any_permission(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        post = PostFactory(user=self.user)
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_retrieve_a_post_created_by_themselves_with_read_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        post = PostFactory(user=self.user)
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

        def test_authenticated_user_can_retrieve_a_post_created_by_themselves_with_edit_permission_and_200_is_returned(self):
            # Arrange
            self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
            post = PostFactory(user=self.user)
            post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
            url = reverse('post-retrieve-update-delete', args=[post.id])
            # Act
            response = self.client.get(url)
            # Assert
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('id'), post.id)

        def test_authenticated_user_can_not_retrieve_a_post_created_by_themselves_without_any_permission_and_404_is_returned(self):
            # Arrange
            self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
            post = PostFactory(user=self.user)
            post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
            url = reverse('post-retrieve-update-delete', args=[post.id])
            # Act
            response = self.client.get(url)
            # Assert
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_another_user_can_not_retrieve_a_post_with_only_read_permission_by_its_author_and_404_is_returned(self):
            # Arrange
            another_user = CustomUserFactory(team=self.team)
            self.client.force_authenticate(another_user)
            self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
            self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
            self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
            self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
            post = PostFactory(user=self.user)
            post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
            url = reverse('post-retrieve-update-delete', args=[post.id])
            # Act
            response = self.client.get(url)
            # Assert
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_another_user_can_not_retrieve_a_post_with_only_edit_permission_by_its_author_and_404_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        post = PostFactory(user=self.user)
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_another_user_can_not_retrieve_a_post_with_no_permissions_by_its_author_and_404_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        post = PostFactory(user=self.user)
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PostAuthenticatedUserDeleteViewTests(APITestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.permissions = PermissionFactory.create_batch()
        self.categories = CategoryFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }
        
    def test_authenticated_user_can_delete_a_post_with_public_edit_permission_and_204_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        current_posts = Post.objects.count()
        expected_permissions = 0
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), current_posts - 1)
        self.assertEqual(post_category_permission_db.count(), expected_permissions)
    
    
    def test_authenticated_user_can_delete_a_post_with_authenticated_edit_permission_and_204_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        expected_category_permission = 0
        current_posts = Post.objects.count()
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), current_posts - 1)
        self.assertEqual(post_category_permission_db.count(), expected_category_permission)
    
    def test_authenticated_user_can_not_delete_post_with_authenticated_read_permission_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        post = PostFactory()
        current_posts = Post.objects.count()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_authenticated_user_can_not_delete_post_with_any_authenticated_permission_at_all_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        current_posts = Post.objects.count()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)

    def test_authenticated_user_can_delete_post_with_team_edit_permission_and_204_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        post = PostFactory(user=self.user)
        current_posts = Post.objects.count()
        expected_permissions = 0
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), current_posts - 1)
        self.assertEqual(post_category_permission_db.count(), expected_permissions)

    def test_authenticated_user_can_not_delete_post_with_team_read_permission_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        post = PostFactory(user=self.user)
        current_posts = Post.objects.count()
        expected_permissions = len(CATEGORIES.keys())
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)
        self.assertEqual(post_category_permission_db.count(), expected_permissions)

    def test_authenticated_user_can_not_delete_post_with_team_no_permission_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        post = PostFactory(user=self.user)
        current_posts = Post.objects.count()
        expected_permissions = len(CATEGORIES.keys())
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)
        self.assertEqual(post_category_permission_db.count(), expected_permissions)

    def test_authenticated_user_can_delete_a_post_with_author_edit_permission_and_204_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        post = PostFactory(user=self.user)
        current_posts = Post.objects.count()
        expected_permissions = 0
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), current_posts - 1)
        self.assertEqual(post_category_permission_db.count(), expected_permissions)

    def test_authenticated_user_can_not_delete_a_post_with_author_read_permission_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        post = PostFactory(user=self.user)
        current_posts = Post.objects.count()
        expected_permissions = len(CATEGORIES.keys())
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)
        self.assertEqual(post_category_permission_db.count(), expected_permissions)

    def test_authenticated_user_can_not_delete_a_post_with_author_no_permissions_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        post = PostFactory(user=self.user)
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        current_posts = Post.objects.count()
        expected_permissions = len(CATEGORIES.keys())
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        post_category_permission_db = PostCategoryPermission.objects.filter(post=post)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)
        self.assertEqual(post_category_permission_db.count(), expected_permissions) 

    def test_authenticated_user_can_not_delete_a_post_that_does_not_exist_and_404_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        post_id = 100
        url = reverse('post-retrieve-update-delete', args=[post_id])
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), current_posts)

class PostAuthenticatedUserUpdateViewTests(APITestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.permissions = PermissionFactory.create_batch()
        self.categories = CategoryFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }

    def test_authenticated_user_can_update_with_put_a_post_with_public_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permission in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])

    def test_authenticated_user_can_update_with_patch_a_post_with_public_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        data = {
            'title': 'New title',
            'content': 'New Content'
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])

    def test_authenticated_user_can_update_with_put_a_post_with_authenticated_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])

    def test_authenticated_user_can_update_with_put_a_post_with_authenticated_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        data = {
            'title': 'New title',
            'content': 'New Content'
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])

    def test_authenticated_user_can_not_update_with_put_a_post_with_public_and_authenticated_read_permissions_and_404_is_returned(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_default_category_permissions_handler(self.categories, self.permissions)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)

    def test_authenticated_user_can_not_updatea_post_without_any_public_and_authenticated_permissions_and_404_is_returned(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)

    def test_authenticated_user_can_not_update_with_patch_a_post_with_public_and_authenticated_read_permissions_and_404_is_returned(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        data = {
            'title': 'New title',
            'content': 'New Content'
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)

    def test_another_authenticated_user_can_update_with_put_a_post_with_team_edit_permission_and_200_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])

    def test_another_authenticated_user_can_update_with_patch_a_post_with_team_edit_permission_and_200_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.EDIT
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        data = {
            'title': 'New title',
            'content': 'New Content'
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])

    def test_another_authenticated_with_same_team_can_not_update_with_put_a_read_only_team_post_and_404_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)

    def test_another_authenticated_with_same_team_can_not_update_with_patch_a_read_only_team_post_and_404_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.READ
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        data = {
            'title': 'New title',
            'content': 'New Content'
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)

    def test_another_authenticated_with_same_team_can_not_update_a_post_without_any_permission_and_404_is_returned(self):
        # Arrange
        another_user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(another_user)
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)

    def test_post_owner_can_edit_with_put_a_post_with_author_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])

    def test_post_owner_can_edit_with_patch_a_post_with_author_edit_permission_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.EDIT
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        data = {
            'title': 'New title',
            'content': 'New Content'
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])

    def test_post_owner_can_not_edit_with_put_a_post_with_author_read_permission_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)

    def test_post_owner_can_not_edit_with_patch_a_post_with_author_read_permission_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.READ
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        data = {
            'title': 'New title',
            'content': 'New Content'
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)
    
    def test_post_owner_can_not_edit_with_put_a_post_with_any_permission_and_404_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        post = PostFactory(user=self.user)
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission should be the same as the current category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(post_db.title, post.title)
        self.assertEqual(post_db.content, post.content)

    def test_authenticated_user_with_permission_can_update_with_put_category_permission_and_then_lost_edit_access(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission is different from category_permissin in the db
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        category_permission_db = PostCategoryPermission.objects.get(post=post, category__name=AccessCategory.AUTHENTICATED)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(category_permission_db.permission.name, AccessPermission.READ)
    
    def test_authenticated_user_with_permission_can_update_with_patch_category_permission_and_then_lost_edit_access(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission is different from category_permissin in the db
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'category_permission': category_permission
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        category_permission_db = PostCategoryPermission.objects.get(post=post, category__name=AccessCategory.AUTHENTICATED)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(category_permission_db.permission.name, AccessPermission.READ)

    def test_authenticated_user_can_not_update_a_post_that_does_not_exist_and_404_is_returned(self):
        # Arrange
        post_id = 100
        url = reverse('post-retrieve-update-delete', args=[post_id])
        data = {
            'title': 'New title',
            'content': 'New Content'
        }
        # Act
        response = self.client.patch(url, data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_send_incomplete_category_permission_with_put_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission is different from category_permissin in the db
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        category_permission.pop(0)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_permissions = PostCategoryPermission.objects.get(post=post, category__name=AccessCategory.AUTHENTICATED)
        post_permission_amount = PostCategoryPermission.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_permissions.permission.name, AccessPermission.READ)
        self.assertEqual(post_permission_amount, len(CATEGORIES.keys()))

    def test_authenticated_user_can_send_incomplete_category_permission_with_patch_and_200_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission is different from category_permissin in the db
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        category_permission.pop(0)
        data = {
            'category_permission': category_permission
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_permissions = PostCategoryPermission.objects.get(post=post, category__name=AccessCategory.AUTHENTICATED)
        post_permission_amount = PostCategoryPermission.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_permissions.permission.name, AccessPermission.READ)
        self.assertEqual(post_permission_amount, len(CATEGORIES.keys()))
    
    def test_authenticated_user_can_not_update_with_an_invalid_permission_id_and_400_is_returned(self):
        # Arrange
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.EDIT
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission is different from category_permissin in the db
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.READ
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        category_permission[0] = {
            "category": "10000",
            "permission": "10000"
        }
        data = {
            'category_permission': category_permission
        }
        # Act
        response = self.client.patch(url, data, format='json')
        post_permissions = PostCategoryPermission.objects.get(post=post, category__name=AccessCategory.AUTHENTICATED)
        post_permission_amount = PostCategoryPermission.objects.count()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post_permissions.permission.name, AccessPermission.EDIT)
        self.assertEqual(post_permission_amount, len(CATEGORIES.keys()))
        
class PostAdminUserViewTests(APITestCase):
    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team, is_staff=True)
        self.client.force_authenticate(self.user)
        self.permissions = PermissionFactory.create_batch()
        self.categories = CategoryFactory.create_batch()
        self.factory_category_permission = {
            AccessCategory.PUBLIC: AccessPermission.READ,
            AccessCategory.AUTHENTICATED: AccessPermission.READ,
            AccessCategory.TEAM: AccessPermission.EDIT,
            AccessCategory.AUTHOR: AccessPermission.EDIT
        }

    def test_admin_user_can_list_all_posts_regardless_of_permissions(self):
        # Arrange
        posts = PostFactory.create_batch(5)
        PostCategoryPermissionFactory.create_batch(posts, category_permission=self.factory_category_permission)
        posts_restricted = PostFactory.create_batch(3)
        restricted_post_permissions = {
            AccessCategory.PUBLIC: AccessPermission.NO_PERMISSION,
            AccessCategory.AUTHENTICATED: AccessPermission.NO_PERMISSION,
            AccessCategory.TEAM: AccessPermission.NO_PERMISSION,
            AccessCategory.AUTHOR: AccessPermission.NO_PERMISSION
        }
        PostCategoryPermissionFactory.create_batch(posts_restricted, category_permission=restricted_post_permissions)
        url = reverse('post-list-create')
        # Act
        response = self.client.get(url, format='json')
        count = response.data.get('count')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, 8)

    def test_admin_user_can_retrieve_any_post_regardless_of_permissions(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)
    
    def test_admin_user_can_update_a_post_with_permission_as_no_permission_and_200_is_returned(self):
        # Arrange
        post = PostFactory()
        self.factory_category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHENTICATED] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.TEAM] = AccessPermission.NO_PERMISSION
        self.factory_category_permission[AccessCategory.AUTHOR] = AccessPermission.NO_PERMISSION
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission is the same from category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])
    
    def test_admin_user_can_update_with_put_a_post_regardless_of_permissions_and_200_is_returned(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # The sending category_permission is the same from category_permissin in the db
        category_permission = create_custom_category_permissions_handler(self.categories, self.permissions, self.factory_category_permission)
        data = {
            'title': 'New title',
            'content': 'New Content',
            'category_permission': category_permission
        }
        # Act
        response = self.client.put(url, data, format='json')
        post_db = Post.objects.get(id=post.id)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), data['title'])
        self.assertEqual(response.data.get('content'), data['content'])
        self.assertEqual(post_db.title, data['title'])
        self.assertEqual(post_db.content, data['content'])


    def test_admin_user_can_delete_any_post_regardless_of_permissions(self):
        # Arrange
        post = PostFactory()
        PostCategoryPermissionFactory(post=post, category_permission=self.factory_category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        current_posts = Post.objects.count()
        # Act
        response = self.client.delete(url, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), current_posts - 1)