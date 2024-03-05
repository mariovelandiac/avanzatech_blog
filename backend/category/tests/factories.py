from factory import Faker
from factory.django import DjangoModelFactory
from category.models import Category
from common.constants import CATEGORIES


class CategoryFactory(DjangoModelFactory):
    name = Faker('random_element', elements=CATEGORIES.keys())
    description = Faker('text')

    class Meta:
        model = Category

    @classmethod
    def create_batch(cls, **kwargs):
        names = CATEGORIES.keys()
        description = list(CATEGORIES.values())
        results = [CategoryFactory.create(name=name, description=description[i]) for i, name in enumerate(names)]
        return results