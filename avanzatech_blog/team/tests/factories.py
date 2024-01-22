from factory.django import DjangoModelFactory
from factory import Faker
from team.models import Team

class TeamFactory(DjangoModelFactory):
    
    name = Faker('word')

    class Meta:
        model = Team