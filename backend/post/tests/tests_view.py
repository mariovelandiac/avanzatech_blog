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
from common.constants import EXCERPT_LENGTH, DEFAULT_ACCESS_CONTROL, CONTENT_MOCK, AccessCategory, AccessPermission
from common.paginator import TenResultsSetPagination

def create_default_category_permissions_handler(categories, permissions):
    read_permission = next((p.id for p in permissions if p.name == AccessPermission.READ), None)
    edit_permission = next((p.id for p in permissions if p.name == AccessPermission.EDIT), None)

    category_permissions = []
    for category in categories:
        permission = read_permission if category.name in [AccessCategory.PUBLIC, AccessCategory.AUTHENTICATED] else edit_permission
        category_permissions.append({"category": category.id, "permission": permission})

    return category_permissions


class PostUnauthenticatedUserCreateViewTests(APITestCase):

    def test_an_unauthenticated_user_can_not_create_a_post_and_a_403_is_returned(self):
        # Arrange
        current_posts = Post.objects.count()
        expected_response = "not_authenticated"
        data = {
            "title": "test title",
            "content": "This is the content of the Post",
            "access_control": DEFAULT_ACCESS_CONTROL,
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
        self.category_permission = DEFAULT_ACCESS_CONTROL

    
    def test_unauthenticated_user_can_see_public_posts_when_posts_have_public_read_permission(self):
        # Arrange
        amount_posts = 4
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        posts = PostFactory.create_batch(amount_posts)
        post_category_permission = PostCategoryPermissionFactory.create_batch(posts, category_permission=self.category_permission)
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
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        posts = PostFactory.create_batch(amount_posts)
        post_category_permission = PostCategoryPermissionFactory.create_batch(posts, category_permission=self.category_permission)
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
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        posts_no_permission = PostFactory.create_batch(no_permission_public_posts)
        post_category_permission = PostCategoryPermissionFactory.create_batch(posts_no_permission, category_permission=self.category_permission)
        read_public_posts = 2
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        posts_read = PostFactory.create_batch(read_public_posts)
        post_category_permission = PostCategoryPermissionFactory.create_batch(posts_read, category_permission=self.category_permission)
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
        self.category_permission = DEFAULT_ACCESS_CONTROL

    def test_unauthenticated_user_receive_user_first_and_last_name_when_lists_public_posts(self):
        # Arrange
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.category_permission)
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
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('excerpt', data)

    def test_unauthenticated_user_can_not_see_post_details_when_post_has_not_public_permission(self):
        # Arrange
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.NO_PERMISSION
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_can_see_post_details_when_post_has_public_read_permission(self):
        # Arrange
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.READ
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

    def test_unauthenticated_user_can_see_post_details_when_post_has_public_edit_permission(self):
        # Arrange
        self.category_permission[AccessCategory.PUBLIC] = AccessPermission.EDIT
        post = PostFactory()
        post_category_permission = PostCategoryPermissionFactory(post=post, category_permission=self.category_permission)
        url = reverse('post-retrieve-update-delete', args=[post.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), post.id)

class PostUnauthenticatedUserEditViewTests(APITestCase):

    def setUp(self):
        self.factory_category_permission = DEFAULT_ACCESS_CONTROL
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
        self.factory_category_permission = DEFAULT_ACCESS_CONTROL
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
    
# class PostUpdateViewTests(APITestCase):

#     def setUp(self):
#         self.user = CustomUserFactory()
#         self.post = PostFactory(user=self.user)
#         self.data = {
#             "title": self.post.title,
#             "content": self.post.content,
#             "read_permission": self.post.read_permission
#         }
#         self.url = reverse('post-retrieve-update-delete', args=[self.post.id])
#         self.client.force_authenticate(self.user)

#     def test_update_the_title_with_put_method_is_allowed_for_owner_of_the_post(self):
#         # Arrange
#         new_title = "this is a new title"
#         self.data['title'] = new_title
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).title, new_title)
#         self.assertEqual(self.post.id, response.data.get('id'))


#     def test_update_the_title_with_patch_method_is_allowed_for_owner_of_the_post(self):
#         # Arrange
#         new_title = "this is a new title"
#         data = {
#             "title": new_title
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).title, new_title)
    

#     def test_update_the_title_with_put_method_is_forbidden_for_another_user_from_the_request_user(self):
#         # Arrange
#         another_user = CustomUserFactory()
#         self.client.force_authenticate(another_user)
#         new_title = "this is a new title"
#         self.data['title'] = new_title
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(last_modified_db, last_modified_db_after_request)
#         self.assertNotEqual(Post.objects.get(id=self.post.id).title, new_title)

#     def test_update_the_title_with_patch_method_is_forbidden_for_another_user_from_the_request_user(self):
#         # Arrange
#         another_user = CustomUserFactory()
#         self.client.force_authenticate(another_user)
#         new_title = "this is a new title"
#         data = {
#             "title": new_title
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(last_modified_db, last_modified_db_after_request)
#         self.assertNotEqual(Post.objects.get(id=self.post.id).title, new_title)

#     def test_update_the_title_with_put_method_and_is_admin_user_is_carried_out_successfully(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         new_title = "this is a new title"
#         self.data['title'] = new_title
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).title, new_title)

#     def test_update_the_title_with_patch_method_and_is_admin_user_is_carried_out_successfully(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         new_title = "this is a new title"
#         data = {
#             "title": new_title
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).title, new_title)

#     def test_update_put_read_permission_is_carried_out_successfully(self):
#         # Arrange
#         for permission in list(READ_PERMISSIONS.keys()):
#             if permission != self.post.read_permission:
#                 self.data['read_permission'] = permission
#                 break
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).read_permission, self.data['read_permission'])


#     def test_update_put_read_permission_by_unauthorized_user_returns_404(self):
#         # Arrange
#         another_user = CustomUserFactory()
#         self.client.force_authenticate(another_user)
#         for permission in list(READ_PERMISSIONS.keys()):
#             if permission != self.post.read_permission:
#                 self.data['read_permission'] = permission
#                 break
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(last_modified_db, last_modified_db_after_request)
#         self.assertNotEqual(Post.objects.get(id=self.post.id).read_permission, self.data['read_permission'])

#     def test_update_put_read_permission_by_admin_is_carried_out_successfully(self):
#         # Arrange
#         another_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(another_user)
#         for permission in list(READ_PERMISSIONS.keys()):
#             if permission != self.post.read_permission:
#                 self.data['read_permission'] = permission
#                 break
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).read_permission, self.data['read_permission'])

#     def test_update_patch_read_permission_is_carried_out_successfully(self):
#         # Arrange
#         new_permission = None
#         for permission in list(READ_PERMISSIONS.keys()):
#             if permission != self.post.read_permission:
#                 new_permission = permission
#                 break
#         data = {
#             "read_permission": new_permission
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).read_permission, new_permission)

#     def test_update_patch_read_permission_by_unauthorized_user_returns_404(self):
#         # Arrange
#         another_user = CustomUserFactory()
#         self.client.force_authenticate(another_user)
#         new_permission = None
#         for permission in list(READ_PERMISSIONS.keys()):
#             if permission != self.post.read_permission:
#                 new_permission = permission
#                 break
#         data = {
#             "read_permission": new_permission
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(last_modified_db, last_modified_db_after_request)
#         self.assertNotEqual(Post.objects.get(id=self.post.id).read_permission, new_permission)

#     def test_update_put_read_permission_with_an_invalid_permission_returns_400(self):
#         # Arrange
#         self.data['read_permission'] = 'invalid permission'
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         post_db = Post.objects.get(id=self.post.id)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertNotEqual(post_db.read_permission, self.data['read_permission'])

#     def test_update_patch_read_permission_by_admin_is_carried_out_successfully(self):
#         # Arrange
#         another_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(another_user)
#         new_permission = None
#         for permission in list(READ_PERMISSIONS.keys()):
#             if permission != self.post.read_permission:
#                 new_permission = permission
#                 break
#         data = {
#             "read_permission": new_permission
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).read_permission, new_permission)

#     def test_update_the_content_with_patch_method_is_allowed_for_owner_of_the_post(self):
#         # Arrange
#         new_content = "This is the new content"
#         self.data['content'] = new_content
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).content, new_content)


#     def test_update_the_content_with_patch_method_is_allowed_for_owner_of_the_post(self):
#         # Arrange
#         new_content = "This is the new content"
#         data = {
#             "content": new_content
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).content, new_content)
    

#     def test_update_the_content_with_put_method_is_forbidden_for_another_user_from_the_request_user(self):
#         # Arrange
#         another_user = CustomUserFactory()
#         self.client.force_authenticate(another_user)
#         new_content = "This is the new content"
#         self.data['content'] = new_content
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(last_modified_db, last_modified_db_after_request)
#         self.assertNotEqual(Post.objects.get(id=self.post.id).content, new_content)

#     def test_update_the_content_with_patch_method_is_forbidden_for_another_user_from_the_request_user(self):
#         # Arrange
#         another_user = CustomUserFactory()
#         self.client.force_authenticate(another_user)
#         new_content = "This is the new content"
#         data = {
#             "content": new_content
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(last_modified_db, last_modified_db_after_request)
#         self.assertNotEqual(Post.objects.get(id=self.post.id).content, new_content)

#     def test_update_the_content_with_put_method_and_is_admin_user_is_carried_out_successfully(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         new_content = "This is the new content"
#         self.data['content'] = new_content
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.put(self.url, self.data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).content, new_content)

#     def test_update_the_content_with_patch_method_and_is_admin_user_is_carried_out_successfully(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         new_content = "This is the new content"
#         data = {
#             "content": new_content
#         }
#         last_modified_db = Post.objects.get(id=self.post.id).last_modified
#         # Act
#         response = self.client.patch(self.url, data)
#         # Assert
#         last_modified_db_after_request = Post.objects.get(id=self.post.id).last_modified
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertLess(last_modified_db, last_modified_db_after_request)
#         self.assertEqual(Post.objects.get(id=self.post.id).content, new_content)


#     def test_update_the_content_with_patch_method_and_is_admin_user_also_updates_the_excerpt(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         new_content = "This is the new content"
#         self.data['content'] = new_content
#         post_db = Post.objects.get(id=self.post.id)
#         # Act
#         response = self.client.put(self.url, self.data)
#         post_db_after_request = Post.objects.get(id=self.post.id)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertNotEqual(post_db.excerpt, post_db_after_request.excerpt)
#         self.assertEqual(post_db_after_request.excerpt, data["content"][:EXCERPT_LENGTH])
#         self.assertLessEqual(len(post_db_after_request.excerpt), EXCERPT_LENGTH)


#     def test_update_the_content_with_patch_method_and_is_admin_user_also_updates_the_excerpt(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         new_content = "This is the new content"
#         data = {
#             "content": new_content
#         }
#         post_db = Post.objects.get(id=self.post.id)
#         # Act
#         response = self.client.patch(self.url, data)
#         post_db_after_request = Post.objects.get(id=self.post.id)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertNotEqual(post_db.excerpt, post_db_after_request.excerpt)
#         self.assertEqual(post_db_after_request.excerpt, data["content"][:EXCERPT_LENGTH])
#         self.assertLessEqual(len(post_db_after_request.excerpt), EXCERPT_LENGTH)


#     def test_update_the_content_with_put_method_and_is_write_public_post_also_updates_the_excerpt(self):
#         pass

#     def test_update_the_content_with_put_method_and_is_write_authenticated_post_also_updates_the_excerpt(self):
#         pass

#     def test_update_the_content_with_put_method_and_is_write_team_post_also_updates_the_excerpt(self):
#         pass

#     def test_update_the_content_with_put_method_and_is_write_author_post_also_updates_the_excerpt(self):
#         pass


# class PostListViewTests(APITestCase):

#     def setUp(self):
#         self.team = TeamFactory()
#         self.user = CustomUserFactory(team=self.team)
#         self.url = reverse('post-list-create')
#         self.client.force_authenticate(self.user)
        

#     def test_anonymous_user_only_can_list_public_posts(self):
#         # Arrange
#         self.client.logout()
#         expected_count = 3
#         PostFactory.create_batch(3, read_permission=ReadPermissions.PUBLIC)
#         PostFactory.create_batch(3, read_permission=ReadPermissions.AUTHENTICATED)
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         self.assertLessEqual(len(results), TenResultsSetPagination.page_size)
#         for post in results:
#             self.assertEqual(post['read_permission'], 'public')
               

#     def test_admin_user_can_list_every_post_regardless_of_the_permission(self):
#         # Arrange
#         PostFactory.create_batch(2, read_permission=ReadPermissions.PUBLIC)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHENTICATED)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.TEAM)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR)
#         expected_count = 8
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for post in results:
#             self.assertNotEqual(admin_user.id, post['user'])

#     def test_logged_in_user_can_list_public_and_authenticated_posts(self):
#         # Arrange
#         PostFactory.create_batch(2, read_permission=ReadPermissions.PUBLIC)
#         PostFactory.create_batch(3, read_permission=ReadPermissions.AUTHENTICATED)
#         expected_count = 5
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for post in results:
#             self.assertNotEqual(post['read_permission'], ReadPermissions.TEAM)
#             self.assertNotEqual(post['read_permission'], ReadPermissions.AUTHOR)

#     def test_logged_in_user_can_list_team_posts(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.TEAM, user=other_user)
#         PostFactory.create_batch(3, read_permission=ReadPermissions.TEAM, user=self.user)
#         expected_count = 5
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for post in results:
#             self.assertNotEqual(post['read_permission'], ReadPermissions.AUTHOR)

#     def test_logged_in_user_can_list_same_team_posts_but_not_those_with_author_permission_by_other_user(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         PostFactory.create_batch(3, read_permission=ReadPermissions.TEAM, user=other_user)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=other_user)
#         expected_count = 3
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         for post in results:
#             self.assertNotEqual(post['read_permission'], ReadPermissions.AUTHOR)

#     def test_logged_in_user_can_list_public_authenticated_team_and_self_posts(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.PUBLIC)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHENTICATED)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.TEAM, user=other_user)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=self.user)
#         expected_count = 8
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_logged_in_user_can_list_team_and_self_posts(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         PostFactory.create_batch(1, read_permission=ReadPermissions.TEAM, user=self.user)
#         PostFactory.create_batch(1, read_permission=ReadPermissions.TEAM, user=other_user)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=self.user)
#         expected_count = 4
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_logged_in_user_can_not_list_author_posts_by_other_user(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=self.user)
#         PostFactory.create_batch(2, read_permission=ReadPermissions.AUTHOR, user=other_user)
#         expected_count = 2
#         # Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)

#     def test_user_without_any_post_available_to_see_will_receive_empty_list(self):
#         # Arrange
#         user = CustomUserFactory()
#         self.client.force_authenticate(user)
#         PostFactory.create_batch(10, read_permission=ReadPermissions.AUTHOR)
#         expected_count = 0
#         #  Act
#         response = self.client.get(self.url)
#         count = response.data.get('count')
#         results = response.data.get('results')
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(count, expected_count)
#         self.assertLessEqual(len(results), expected_count)
       
# class PostRetrieveViewTests(APITestCase):

#     def setUp(self):
#         self.team = TeamFactory()
#         self.user = CustomUserFactory(team=self.team)
#         self.client.force_authenticate(self.user)

#     def test_anonymous_user_can_retrieve_a_public_post(self):
#         # Arrange
#         self.client.logout()
#         post = PostFactory(read_permission=ReadPermissions.PUBLIC)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)  
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

#     def test_anonymous_user_can_not_retrieve_an_authenticated_post(self):
#         # Arrange
#         self.client.logout()
#         post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_anonymous_user_can_not_retrieve_a_team_post(self):
#         # Arrange
#         self.client.logout()
#         post = PostFactory(read_permission=ReadPermissions.TEAM)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


#     def test_anonymous_user_can_not_retrieve_an_author_post(self):
#         # Arrange
#         self.client.logout()
#         post = PostFactory(read_permission=ReadPermissions.AUTHOR)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_logged_in_user_can_retrieve_a_public_post(self):
#         # Arrange
#         post = PostFactory(read_permission=ReadPermissions.PUBLIC)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

#     def test_logged_in_user_can_retrieve_an_authenticated_post(self):
#         # Arrange
#         post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

#     def test_logged_in_user_can_retrieve_a_team_post_when_the_user_is_in_the_same_team(self):
#         # Arrange
#         other_user = CustomUserFactory(team=self.team)
#         post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

#     def test_logged_in_user_can_not_retrieve_a_team_post_if_the_user_does_not_belong_to_that_team(self):
#         # Arrange
#         other_user = CustomUserFactory()
#         post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_logged_in_user_can_retrieve_an_author_post_when_the_user_wrote_it(self):
#         # Arrange
#         post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=self.user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

#     def test_logged_in_user_can_not_retrieve_an_author_post_when_the_user_does_not_wrote_it(self):
#         # Arrange
#         other_user = CustomUserFactory()
#         post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=other_user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_logged_in_user_can_retrieve_a_public_post_if_was_written_by_themselves(self):
#         # Arrange
#         post = PostFactory(read_permission=ReadPermissions.PUBLIC, user=self.user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

#     def test_logged_in_user_can_retrieve_an_authenticated_post_if_was_written_by_themselves(self):
#         # Arrange
#         post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

#     def test_logged_in_user_can_retrieve_a_team_post_if_was_written_by_themselves(self):
#         # Arrange
#         post = PostFactory(read_permission=ReadPermissions.TEAM, user=self.user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)        
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)


#     def test_admin_user_can_retrieve_a_public_post(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         post = PostFactory(read_permission=ReadPermissions.PUBLIC)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)        
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

#     def test_admin_user_can_retrieve_an_authenticated_post(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)        
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)
        

#     def test_admin_user_can_retrieve_a_team_post(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         post = PostFactory(read_permission=ReadPermissions.TEAM, user=self.user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)        
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)
        

#     def test_admin_user_can_retrieve_an_author_post(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=self.user)
#         url = reverse('post-retrieve-update-delete', args=[post.id])
#         # Act & Assert
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(response.data)
#         self.assertEqual(response.data.get('user'), post.user.id)
#         self.assertEqual(response.data.get('read_permission'), post.read_permission)
#         self.assertEqual(response.data.get('id'), post.id)
#         self.assertEqual(response.data.get('title'), post.title)
#         self.assertEqual(response.data.get('content'), post.content)        
#         self.assertEqual(response.data.get('excerpt'), post.excerpt)
#         self.assertLessEqual(len(response.data.get('excerpt')), EXCERPT_LENGTH)

# class PostDeleteViewTests(APITestCase):
    
#     def setUp(self):
#         self.team = TeamFactory()
#         self.user = CustomUserFactory(team=self.team)
#         self.post = PostFactory(user=self.user, read_permission=ReadPermissions.PUBLIC)
#         self.url = "post-retrieve-update-delete"
#         self.client.force_authenticate(self.user)

#     def test_unauthenticated_user_can_not_delete_posts(self):
#         # Arrange
#         self.client.logout()
#         url = reverse(self.url, kwargs={"pk": self.post.id})
#         expected_count = 1
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(Post.objects.count(), expected_count)

#     def test_logged_in_user_can_not_delete_a_post_that_does_not_belong_to_themselves(self):
#         # Arrange
#         other_user = CustomUserFactory()
#         self.client.force_authenticate(other_user)
#         url = reverse(self.url, kwargs={"pk": self.post.id})
#         expected_count = 1
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(Post.objects.count(), expected_count)

#     def test_logged_in_user_can_delete_a_post_that_belong_to_themselves(self):
#         # Arrange
#         url = reverse(self.url, kwargs={"pk": self.post.id})
#         expected_count = 0
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Post.objects.count(), expected_count)

#     def test_logged_in_user_delete_a_post_and_likes_and_comments_are_also_destroyed(self):
#         # Arrange
#         LikeFactory.create_batch(2, post=self.post)
#         CommentFactory.create_batch(2, post=self.post)
#         url = reverse(self.url, kwargs={"pk": self.post.id})
#         expected_count = 0
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Post.objects.count(), expected_count)
#         self.assertEqual(Comment.objects.count(), expected_count)
#         self.assertEqual(Like.objects.count(), expected_count)

#     def test_admin_user_can_delete_any_post_regardless_of_permission(self):
#         # Arrange
#         admin_user = CustomUserFactory(is_staff=True)
#         self.client.force_authenticate(admin_user)
#         LikeFactory.create_batch(2, post=self.post)
#         CommentFactory.create_batch(2, post=self.post)
#         url = reverse(self.url, kwargs={"pk": self.post.id})
#         expected_count = 0
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Post.objects.count(), expected_count)
#         self.assertEqual(Comment.objects.count(), expected_count)
#         self.assertEqual(Like.objects.count(), expected_count)

#     def test_logged_in_user_try_to_delete_a_non_existing_post_and_404_is_returned(self):
#         # Arrange
#         post = Post.objects.get(id=self.post.id)
#         post.delete()
#         url = reverse(self.url, kwargs={"pk": self.post.id})
#         expected_count = 0
#         # Act
#         response = self.client.delete(url)
#         # Assert
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(Post.objects.count(), expected_count)




