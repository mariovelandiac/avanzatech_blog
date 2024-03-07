from factory import Faker
from factory.django import DjangoModelFactory
from permission.models import Permission
from common.constants import PERMISSIONS


class PermissionFactory(DjangoModelFactory):
    name = Faker('random_element', elements=PERMISSIONS.keys())
    description = Faker('sentence')

    class Meta:
        model = Permission

    @classmethod
    def create_batch(cls, **kwargs):
        names = PERMISSIONS.keys()
        results = [cls.create(name=name, description=PERMISSIONS[name]) for name in names]
        return results