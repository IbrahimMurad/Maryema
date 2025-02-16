import factory

from product.models import Color


class ColorFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Color instances for testing.
    """

    class Meta:
        model = Color

    color1_name = factory.Faker("color_name")
    color1_value = factory.Faker("hex_color")

    class Params:
        dual = factory.Trait(
            color2_name=factory.Faker("color_name"),
            color2_value=factory.Faker("hex_color"),
        )
