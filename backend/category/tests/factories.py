from factory import Faker
from factory.django import DjangoModelFactory
from category.models import Category
from common.constants import CATEGORIES


class CategoryFactory(DjangoModelFactory):
    name = Faker('random_element', elements=CATEGORIES.keys())
    description = Faker('sentence')

    class Meta:
        model = Category

    @classmethod
    def create_batch(cls, **kwargs):
        names = CATEGORIES.keys()
        results = [cls.create(name=name, description=CATEGORIES[name]) for name in names]
        return results