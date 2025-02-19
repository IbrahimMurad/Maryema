import random

from factory import Faker, LazyFunction, Sequence, SubFactory, Trait, lazy_attribute
from factory.django import DjangoModelFactory

from core.utils import create_image
from product.models import (
    Category,
    Collection,
    Color,
    Division,
    Img,
    Product,
    ProductVariant,
    Size,
)


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


class SizeFactory(DjangoModelFactory):
    class Meta:
        model = Size

    name = Sequence(lambda n: ["XS", "S", "M", "L", "XL", "XXL", "12", "30", "24"][n])


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
    name = Sequence(lambda n: f"Product {n}")
    description = Faker("text", max_nb_chars=200)
    tags = LazyFunction(lambda: ",".join([f"tag{i}" for i in range(3)]))


class ImgFactory(DjangoModelFactory):
    class Meta:
        model = Img

    @lazy_attribute
    def src(self):
        return create_image()

    alt = Sequence(lambda n: f"test-image-{n}")


class VariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = SubFactory(ProductFactory)
    color = SubFactory(ColorFactory)
    image = SubFactory(ImgFactory)
    cost = Faker("random_int", min=10, max=1000)
    quantity = Faker("random_int", min=1, max=100)
    sort_order = Sequence(lambda n: n)

    @lazy_attribute
    def price(self):
        # Ensure price is always higher than cost
        return self.cost + random.randint(50, 300)

    @lazy_attribute
    def size(self):
        return Size.objects.order_by("?").first()


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    name = Sequence(lambda n: f"Collection {n}")
    description = Faker("text", max_nb_chars=200)

    # I will add products to the collection in the test by hand
