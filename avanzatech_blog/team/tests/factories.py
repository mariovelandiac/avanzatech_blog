from factory.django import DjangoModelFactory
from factory import Sequence
from team.models import Team

class TeamFactory(DjangoModelFactory):
    
    name = Sequence(lambda n: f'Team-{n}')
    
    class Meta:
        model = Team