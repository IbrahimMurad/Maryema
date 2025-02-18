from factory import Faker, LazyFunction, Sequence, SubFactory, Trait, lazy_attribute
from factory.django import DjangoModelFactory

from core.utils import create_image
from product.models import Category, Color, Division, Img, Product


class ColorFactory(DjangoModelFactory):
    class Meta:
        model = Color

    color1_name = Faker("color_name")
    color1_value = Faker("hex_color")

    class Params:
        dual = Trait(
            color2_name=Faker("color_name"),
            color2_value=Faker("hex_color"),
        )


class DivisionFactory(DjangoModelFactory):
    class Meta:
        model = Division

    name = Sequence(lambda n: f"Division {n}")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    division = SubFactory(DivisionFactory)
    name = Sequence(lambda n: f"Category {n}")
    description = Faker("text", max_nb_chars=200)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = SubFactory(CategoryFactory)
    name = Faker("product_name")
    description = Faker("text", max_nb_chars=200)
    tags = LazyFunction(lambda: ",".join(Faker("words", nb=3).generate({})))


class ImgFactory(DjangoModelFactory):
    class Meta:
        model = Img

    @lazy_attribute
    def src(self):
        return create_image()

    alt = Sequence(lambda n: f"test-image-{n}")
