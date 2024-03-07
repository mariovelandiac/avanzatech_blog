from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, LazyAttribute
from post.models import Post, PostCategoryPermission
from user.tests.factories import CustomUserFactory  
from category.models import Category
from category.tests.factories import CategoryFactory
from permission.models import Permission
from permission.tests.factories import PermissionFactory
from common.constants import CATEGORIES, EXCERPT_LENGTH, DEFAULT_ACCESS_CONTROL, WORDS_MOCK_TEXT

class PostFactory(DjangoModelFactory):
    
    user = SubFactory(CustomUserFactory)
    title = Faker('sentence')
    content = Faker('sentence', nb_words=WORDS_MOCK_TEXT)
    excerpt = LazyAttribute(lambda obj: obj.content[:EXCERPT_LENGTH])
    class Meta:
        model = Post

class PostCategoryPermissionFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)
    category = SubFactory(CategoryFactory)
    permission = SubFactory(PermissionFactory)

    class Meta:
        model = PostCategoryPermission

    @classmethod
    def create(cls, **kwargs):
        access = []
        access_control = DEFAULT_ACCESS_CONTROL if not kwargs.get('access_control') else kwargs.get('access_control')
        post = PostFactory.create() if not kwargs.get('post') else kwargs.get('post')
        for category, permission in access_control.items():
            category = Category.objects.get(name=category)
            permission = Permission.objects.get(name=permission)
            post_category_permission = PostCategoryPermission.objects.create(post=post, category=category, permission=permission)
            access.append(post_category_permission)
        return access
    
    @classmethod
    def create_batch(cls, posts, **kwargs):
        batch = []
        for post in posts:
            batch.append(cls.create(post=post, **kwargs))
        return batch

    
