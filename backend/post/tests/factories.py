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
    
    @classmethod
    def create(cls, **kwargs):
        post = super().create(**kwargs)
        if not kwargs.get('access_control'):
            kwargs['access_control'] = DEFAULT_ACCESS_CONTROL
        return PostFactory._set_access_control(post, kwargs['access_control'])

    @classmethod
    def _set_access_control(cls, post, access_control):
        for category, permission in access_control.items():
            post_category_permission = PostCategoryPermissionFactory(
                post=post,
                category=Category.objects.get(name=category),
                permission=Permission.objects.get(name=permission)
            )
            post_category_permission.save()
        return post

    class Meta:
        model = Post

class PostCategoryPermissionFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)
    category = SubFactory(CategoryFactory)
    permission = SubFactory(PermissionFactory)

    class Meta:
        model = PostCategoryPermission

    
