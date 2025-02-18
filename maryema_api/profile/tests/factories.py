from profile.models import Profile

from django.contrib.auth.models import User
from factory import Faker, PostGenerationMethodCall, SubFactory, Trait
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = Faker("email")
    password = PostGenerationMethodCall("set_password", "testpass123")
    first_name = Faker("first_name")
    last_name = Faker("last_name")


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = SubFactory(UserFactory)
    phone_number = Faker("bothify", text="+20????????##")
    note = Faker("text", max_nb_chars=200)
    role = Profile.RoleChoices.CUSTOMER

    class Params:
        admin = Trait(
            role=Profile.RoleChoices.ADMIN,
        )
