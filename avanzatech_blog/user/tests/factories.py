from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from user.models import CustomUser
from team.tests.factories import TeamFactory

class CustomUserFactory(DjangoModelFactory):
    
    username = Faker('name')
    email = Faker('email')
    password = Faker('password')
    team = SubFactory(TeamFactory)

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


