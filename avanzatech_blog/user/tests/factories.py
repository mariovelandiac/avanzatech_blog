from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from user.models import CustomUser
from team.tests.factories import TeamFactory

class CustomUserFactory(DjangoModelFactory):
    
    email = Faker('email')
    password = Faker('password')
    team = SubFactory(TeamFactory)

    class Meta:
        model = CustomUser



