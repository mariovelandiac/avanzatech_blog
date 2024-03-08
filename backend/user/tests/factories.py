from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, Sequence
from user.models import CustomUser
from team.tests.factories import TeamFactory

class CustomUserFactory(DjangoModelFactory):
    
    username = Sequence(lambda n: f'username{n}')
    email = Sequence(lambda n: f'user{n}@example.com')
    password = Faker('password')
    team = SubFactory(TeamFactory)
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    class Meta:
        model = CustomUser

    """
    Override the default _create method to use create_user.
    """
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


