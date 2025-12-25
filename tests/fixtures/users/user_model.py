import factory.fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.users.user_profile.models import UserProfileModel

faker = FakerFactory.create()


EXISTS_GOOGLE_USER_ID = 10
EXISTS_GOOGLE_USER_EMAIL = "test@test.com"


@register(_name="user_profile")
class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfileModel

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())
    google_access_token = factory.LazyFunction(lambda: faker.sha256())
