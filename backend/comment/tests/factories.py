from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from comment.models import Comment
from post.tests.factories import PostFactory
from user.tests.factories import CustomUserFactory

class CommentFactory(DjangoModelFactory):

    post = SubFactory(PostFactory)    
    user = SubFactory(CustomUserFactory)
    content = Faker('text')

    class Meta:
        model = Comment