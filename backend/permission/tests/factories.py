from factory import Faker
from factory.django import DjangoModelFactory
from permission.models import Permission
from common.constants import PERMISSIONS


class PermissionFactory(DjangoModelFactory):
    name = Faker('random_element', elements=PERMISSIONS.keys())
    description = Faker('text')

    class Meta:
        model = Permission

    @classmethod
    def create_batch(cls, **kwargs):
        names = PERMISSIONS.keys()
        description = list(PERMISSIONS.values())
        results = [PermissionFactory.create(name=name, description=description[i]) for i, name in enumerate(names)]
        return results