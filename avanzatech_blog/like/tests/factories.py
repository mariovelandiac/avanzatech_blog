from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from like.models import Like
from user.tests.factories import CustomUserFactory
from post.tests.factories import PostFactory

class LikeFactory(DjangoModelFactory):

    user = SubFactory(CustomUserFactory)
    post = SubFactory(PostFactory)

    class Meta:
        model = Like