from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from post.tests.factories import PostFactory
from post.models import Post
from user.tests.factories import CustomUserFactory
from user.models import CustomUser
from team.tests.factories import TeamFactory
from common.constants import ReadPermissions, Status
from comment.models import Comment
from comment.tests.factories import CommentFactory

class CommentCreateViewTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.post = PostFactory(user=self.user)
        self.client.force_authenticate(self.user)
        self.data = {
            "content": "comment body",
            "post": self.post.id,
            "user": self.user.id
        }
        self.url = reverse('comment-list-create')
    
    def test_unauthenticated_user_can_not_create_a_comment(self):
        # Arrange
        self.client.logout()
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_create_a_comment_in_a_post_created_by_themselves_regardless_of_permission(self):
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id)
        self.assertEqual(response.data.get('post'), self.post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertEqual(response.data.get('username'), self.user.username)

    def test_logged_in_user_can_create_more_than_one_comment_to_one_post(self):
        # Act
        response1 = self.client.post(self.url, self.data)
        response2 = self.client.post(self.url, self.data)
        expected_comments_db = 2
        # Assert
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response1.data['id'], response2.data['id'])
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_logged_in_user_can_create_a_comment_in_a_public_post(self):
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
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertEqual(response.data.get('username'), self.user.username)

    def test_logged_in_user_can_create_a_comment_in_an_authenticated_post(self):
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
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertEqual(response.data.get('username'), self.user.username)
    
    def test_logged_in_user_can_create_a_comment_in_a_team_post_if_belongs_to_same_team(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
        self.data['post'] = post.id
        expected_comments_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id) # Created by the authenticated user
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertEqual(response.data.get('username'), self.user.username)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_logged_in_user_can_not_create_a_comment_a_in_a_team_post_if_does_not_belongs_to_that_team(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory(read_permission=ReadPermissions.TEAM, user=other_user)
        self.data['post'] = post.id
        expected_comments_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_logged_in_user_can_not_create_a_comment_in_a_author_post_that_does_not_belong_themselves(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=other_user)
        self.data['post'] = post.id
        expected_comments_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_logged_in_user_can_create_a_comment_in_a_author_post_that_belongs_themselves(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=self.user)
        self.data['post'] = post.id
        expected_comments_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), self.user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertEqual(response.data.get('username'), self.user.username)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_a_logged_in_user_can_not_create_a_comment_in_a_post_that_does_not_exist(self):
        # Arrange
        self.data['post'] = self.post.id + 1 # this post doesn't exist
        expected_comments_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_invalid_data_returns_a_404_status_code(self):
        # Arrange
        data = {
                "post_id": self.post.id,
                "user_id": self.user.id
                }
        expected_comments_db = 0
        # Act
        response = self.client.post(self.url, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_admin_user_can_create_a_comment_in_public_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_comments_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertEqual(response.data.get('username'), admin_user.username)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_admin_user_can_create_a_comment_in_an_authenticated_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_comments_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertEqual(response.data.get('username'), admin_user.username)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_admin_user_can_create_a_comment_in_a_team_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.TEAM)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_comments_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertEqual(response.data.get('username'), admin_user.username)
        self.assertEqual(Comment.objects.count(), expected_comments_db)
    
    def test_admin_user_can_create_a_comment_in_an_author_post(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        post = PostFactory(read_permission=ReadPermissions.AUTHOR)
        self.data['post'] = post.id
        self.data['user'] = admin_user.id
        expected_comments_db = 1   
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('user'), admin_user.id)
        self.assertEqual(response.data.get('post'), post.id)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(response.data.get('is_active'), Status.ACTIVE)
        self.assertIsNotNone(response.data.get('created_at'))
        self.assertEqual(response.data.get('username'), admin_user.username)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_comment_with_invalid_user_in_payload_should_return_400(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory(read_permission=ReadPermissions.PUBLIC)
        self.data['user'] = other_user.id
        self.data['post'] = post.id
        expected_comments_db = 0
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

    def test_logged_in_user_can_not_create_a_comment_with_payload_inactive(self):
        # Arrange
        self.data['is_active'] = False
        expected_comments_db = 1
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        comment_db_count = Comment.objects.count()
        comment_db = Comment.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment_db_count, expected_comments_db)
        self.assertIs(comment_db.is_active, not self.data['is_active'])

    def test_logged_in_user_can_not_create_a_comment_in_a_valid_post_with_other_user_in_payload(self):
        # Arrange
        other_user = CustomUserFactory()
        post = PostFactory(read_permission=ReadPermissions.PUBLIC, user=other_user)
        self.data['post'] = post.id
        self.data['user'] = other_user.id
        expected_comments_db = 0   
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), expected_comments_db)

class CommentListViewTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.client.force_authenticate(self.user)
        self.url = reverse('comment-list-create')

    def test_unauthenticated_user_can_see_only_public_comments(self):
        # Arrange
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR)
        expected_count = 2
        self.client.logout()
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            post_db = Post.objects.get(id=comment['post'])
            self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)

    def test_logged_in_user_can_list_comments_with_public_and_authenticated_associated_post(self):
        # Arrange
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED)
        expected_count = 4
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_logged_in_user_only_can_see_comments_with_team_permission_by_the_same_team(self):
        # Arrange
        other_team = TeamFactory()
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user__team=self.team)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user__team=other_team)
        expected_count = 2
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            user_db = CustomUser.objects.get(id=comment['user'])
            self.assertEqual(user_db.team.id, self.team.id)

    def test_logged_in_user_only_can_see_comments_with_author_permission_post_by_the_same_author(self):
        # Arrange
        other_user = CustomUserFactory()
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=other_user)
        expected_count = 2
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            user_db = CustomUser.objects.get(id=comment['user'])
            self.assertEqual(user_db.id, self.user.id)

    def test_logged_in_user_can_list_comments_with_team_permission_post_but_not_author_by_the_same_user(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user=other_user)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=other_user)
        expected_count = 2
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            post_db = Post.objects.get(id=comment['post'])
            self.assertEqual(post_db.read_permission, ReadPermissions.TEAM)

    def test_logged_in_user_can_list_public_authenticated_team_and_self_comments(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user=other_user)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user)
        expected_count = 8
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_logged_in_user_can_list_team_and_self_comments(self):
        # Arrange
        other_user = CustomUserFactory(team=self.team)
        CommentFactory.create_batch(1, post__read_permission=ReadPermissions.TEAM, user=self.user)
        CommentFactory.create_batch(1, post__read_permission=ReadPermissions.TEAM, user=other_user)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user)
        expected_count = 4
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_user_without_any_comment_available_to_see_will_receive_empty_list(self):
        # Arrange
        user = CustomUserFactory()
        self.client.force_authenticate(user)
        CommentFactory.create_batch(10, post__read_permission=ReadPermissions.AUTHOR, user=self.user)
        expected_count = 0
        #  Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_admin_user_can_list_every_comment_regardless_of_the_posts_permissions(self):
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR)
        expected_count = 8
        #  Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_admin_user_can_list_self_comments(self):
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        CommentFactory.create_batch(3, user=admin_user)
        expected_count = 3
        #  Act
        response = self.client.get(self.url)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            self.assertEqual(admin_user.id, comment['user'])

    def test_unauthenticated_user_can_filter_public_comments_by_user_id(self):
        # Arrange
        self.client.logout()
        other_user = CustomUserFactory()
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=other_user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=other_user)
        query_params = {
            'user': self.user.id,
        }
        expected_count = 3
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            post_db = Post.objects.get(id=comment['post'])
            user_db = CustomUser.objects.get(id=comment['user'])
            self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)
            self.assertEqual(user_db.id, self.user.id)

    def test_unauthenticated_user_can_filter_public_comments_by_post_id(self):
        # Arrange
        self.client.logout()
        post_public = PostFactory(read_permission=ReadPermissions.PUBLIC)
        CommentFactory.create_batch(3, post=post_public)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED)

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
        for comment in results:
            post_db = Post.objects.get(id=comment['post'])
            self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)

    def test_unauthenticated_user_can_filter_public_comments_by_user_id_and_post_id(self):
        # Arrange
        self.client.logout()
        other_user = CustomUserFactory()
        post_public = PostFactory(read_permission=ReadPermissions.PUBLIC)
        CommentFactory.create_batch(3, post=post_public, user=self.user)
        CommentFactory.create_batch(3, post=post_public) 
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
        query_params = {
            'user': self.user.id,
            'post': post_public.id
        }
        expected_count = 3
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            self.assertEqual(comment['user'], self.user.id)
            self.assertEqual(comment['post'], post_public.id)
            post_db = Post.objects.get(id=comment['post'])
            self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)

    def test_logged_in_user_can_filter_public_and_authenticated_comments_by_user_id(self):
        # Arrange
        other_user = CustomUserFactory()
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=other_user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=other_user)
        query_params = {
            'user': self.user.id,
        }
        expected_count = 6
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            user_db = CustomUser.objects.get(id=comment['user'])
            self.assertEqual(user_db.id, self.user.id)

    def test_logged_in_user_can_filter_public_and_authenticated_comments_by_post_id(self):
        # Arrange
        other_user = CustomUserFactory()
        post_auth = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
        CommentFactory.create_batch(3, post=post_auth)
        CommentFactory.create_batch(3)

        query_params = {
            'post': post_auth.id,
        }
        expected_count = 3
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            self.assertEqual(comment['post'], post_auth.id)

    def test_logged_in_user_can_filter_public_comments_by_user_id_and_post_id(self):
        # Arrange
        other_user = CustomUserFactory()
        post_public = PostFactory(read_permission=ReadPermissions.AUTHENTICATED)
        comment = CommentFactory.create_batch(3, post=post_public, user=self.user)
        CommentFactory.create_batch(3, post=post_public) 
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user)
        query_params = {
            'user': self.user.id,
            'post': post_public.id
        }
        expected_count = 3
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            self.assertEqual(comment['user'], self.user.id)
            self.assertEqual(comment['post'], post_public.id)

    def test_logged_in_user_can_filter_comments_by_user_id(self):
        # Arrange
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user) 
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user=self.user) 
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user) 
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user) 
        CommentFactory.create_batch(7)
        query_params = {
            'user': self.user.id,
        }
        expected_count = 10
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            self.assertEqual(comment['user'], self.user.id)

    def test_logged_in_user_can_filter_comments_by_post_id_with_team_permission_post(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.TEAM, user__team=self.team)
        CommentFactory.create_batch(3, post=post, user__team=self.team) 
        CommentFactory.create_batch(3)
        query_params = {
            'post': post.id,
        }
        expected_count = 3
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            post_db = Post.objects.get(id=comment['post'])
            self.assertEqual(post_db.read_permission, ReadPermissions.TEAM)

    def test_logged_in_user_can_filter_comments_by_post_id_with_author_permission_post(self):
        # Arrange
        post = PostFactory(read_permission=ReadPermissions.AUTHOR, user=self.user)
        CommentFactory.create_batch(3, post=post, user=self.user) 
        CommentFactory.create_batch(3)
        query_params = {
            'post': post.id,
        }
        expected_count = 3
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            self.assertEqual(comment['user'], self.user.id)
            self.assertEqual(comment['post'], post.id)

    def test_admin_user_can_filter_comments_by_user_id_regardless_of_permission(self):
        # Arrange
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, user=self.user) 
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, user=self.user) 
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, user=self.user) 
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, user=self.user) 
        CommentFactory.create_batch(3)
        query_params = {
            'user': self.user.id,
        }
        admin_user=CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        expected_count = 10
        # Act
        response = self.client.get(self.url, data=query_params)
        count = response.data.get('count')
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

    def test_unauthenticated_user_only_can_list_active_public_post_comments(self):
        # Arrange
        self.client.logout()
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, is_active=True)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, is_active=False)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=True)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=False)
        expected_count = 3
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            post_db = Post.objects.get(id=comment['post'])
            self.assertIs(comment['is_active'], True)
            self.assertEqual(post_db.read_permission, ReadPermissions.PUBLIC)

    def test_logged_in_user_only_can_list_active_public_and_authenticated_post_comments(self):
        # Arrange
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, is_active=True)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.PUBLIC, is_active=False)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=True)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=False)
        expected_count = 6
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            self.assertIs(comment['is_active'], True)

    def test_logged_in_user_can_only_list_active_same_team_comments(self):
        # Arrange
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=True, user=self.user, post__user__team=self.team)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=True, user__team=self.team, post__user__team=self.team)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=False, user=self.user, post__user__team=self.team)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=True)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.TEAM, is_active=False)
        expected_count = 6
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

        for comment in results:
            post_db = Post.objects.get(id=comment['post'])
            self.assertIs(comment['is_active'], True)
            self.assertEqual(post_db.read_permission, ReadPermissions.TEAM)
            self.assertEqual(post_db.user.team.id, self.team.id)

    def test_logged_in_user_can_only_list_active_author_team(self):
        # Arrange
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHOR, is_active=True, user=self.user, post__user=self.user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHOR, is_active=False, user=self.user, post__user=self.user)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHOR, is_active=True)
        CommentFactory.create_batch(3, post__read_permission=ReadPermissions.AUTHOR, is_active=False)
        expected_count = 3
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)
        for comment in results:
            post_db = Post.objects.get(id=comment['post'])
            self.assertIs(comment['is_active'], True)
            self.assertEqual(post_db.read_permission, ReadPermissions.AUTHOR)
            self.assertEqual(post_db.user.id, self.user.id)

    def test_admin_user_can_list_active_and_inactive_comments(self):
        # Arrange
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC, is_active=True)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.PUBLIC, is_active=False)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=True)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHENTICATED, is_active=False)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, is_active=True)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.TEAM, is_active=False)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, is_active=False)
        CommentFactory.create_batch(2, post__read_permission=ReadPermissions.AUTHOR, is_active=False)
        expected_count = 16
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        # Act
        response = self.client.get(self.url)
        count = response.data.get('count')    
        results = response.data.get('results')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, expected_count)

class CommentDeleteViewTests(APITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = CustomUserFactory(team=self.team)
        self.post = PostFactory(user=self.user, read_permission=ReadPermissions.PUBLIC)
        self.comment = CommentFactory(user=self.user, post=self.post)
        self.client.force_authenticate(self.user)
        self.url = 'comment-delete'


    def test_unauthenticated_user_can_not_delete_a_active_public_comment(self):
        # Assert
        self.client.logout()
        url = reverse(self.url, kwargs={"pk": self.comment.id})
        # Act
        response = self.client.delete(url)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_logged_in_user_can_delete_a_comment_created_by_themselves(self):
        # Arrange
        url = reverse(self.url, kwargs={"pk": self.comment.id})
        expected_count = 1
        # Act
        response = self.client.delete(url)
        # Assert
        comment_db_count = Comment.objects.count()
        comment_db = Comment.objects.filter(id=self.comment.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(len(comment_db), 0)
        self.assertEqual(comment_db_count, expected_count)
        self.assertFalse(comment_db[0].is_active)


    def test_logged_in_user_can_not_delete_comment_created_by_other_user(self):
        # Arrange
        other_user = CustomUserFactory()
        self.client.force_authenticate(other_user)
        url = reverse(self.url, kwargs={"pk": self.comment.id})
        expected_count = 1
        # Act
        response = self.client.delete(url)
        # Assert
        comment_db_count = Comment.objects.count()
        comment_db = Comment.objects.filter(id=self.comment.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(len(comment_db), 0)
        self.assertEqual(comment_db_count, expected_count)
        self.assertTrue(comment_db[0].is_active)


    def test_admin_user_can_update_any_comment_regardless_of_permissions(self):
        # Arrange
        admin_user = CustomUserFactory(is_staff=True)
        self.client.force_authenticate(admin_user)
        url = reverse(self.url, kwargs={"pk": self.comment.id})
        expected_count = 1
        # Act
        response = self.client.delete(url)
        # Assert
        comment_db_count = Comment.objects.count()
        comment_db = Comment.objects.filter(id=self.comment.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(len(comment_db), 0)
        self.assertEqual(comment_db_count, expected_count)
        self.assertFalse(comment_db[0].is_active)

    def test_logged_in_user_can_not_delete_comment_with_invalid_lookup_fields_invalid(self):
        # Arrange
        url = reverse(self.url, kwargs={"pk": self.comment.id + 1}) # This comment does not exists
        expected_count = 1
        # Act
        response = self.client.delete(url)
        # Assert
        comment_db_count = Comment.objects.count()
        comment_db = Comment.objects.filter(id=self.comment.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(len(comment_db), 0)
        self.assertEqual(comment_db_count, expected_count)
        self.assertTrue(comment_db[0].is_active)






