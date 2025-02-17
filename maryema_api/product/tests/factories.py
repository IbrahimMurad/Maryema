import factory

from core.utils import create_image
from product.models import Color, Img


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


class ImgFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Img

    @factory.lazy_attribute
    def src(self):
        return create_image()

    alt = factory.Sequence(lambda n: f"test-image-{n}")
