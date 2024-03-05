from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, LazyAttribute
from post.models import Post
from common.constants import READ_PERMISSIONS, EXCERPT_LENGTH
from user.tests.factories import CustomUserFactory  

WORDS_FAKE_TEXT = 100
class PostFactory(DjangoModelFactory):
    
    user = SubFactory(CustomUserFactory)
    title = Faker('sentence')
    content = Faker('sentence', nb_words=WORDS_FAKE_TEXT)
    excerpt = LazyAttribute(lambda obj: obj.content[:EXCERPT_LENGTH])
    read_permission = Faker('random_element', elements = list(READ_PERMISSIONS.keys()))

    class Meta:
        model = Post