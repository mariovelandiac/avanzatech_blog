from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from post.models import Post
from post.constants import READ_PERMISSIONS
from user.tests.factories import CustomUserFactory  

class PostFactory(DjangoModelFactory):
    
    user = SubFactory(CustomUserFactory)
    title = Faker('sentence')
    content = Faker('text')
    read_permission = Faker('random_element', elements = list(READ_PERMISSIONS.keys()))

    class Meta:
        model = Post