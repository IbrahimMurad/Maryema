import os
from decimal import Decimal

from django.test import RequestFactory, TestCase

from product.models import Color, Size
from product.serializers import ProductDetailVariantSerializer, VariantSerializer
from product.tests.factories import (
    ColorFactory,
    ImgFactory,
    ProductFactory,
    SizeFactory,
    VariantFactory,
)


class VariantSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        SizeFactory.create_batch(5)
        cls.product = ProductFactory()
        cls.variants = VariantFactory.create_batch(5, product=cls.product)
        cls.request = RequestFactory().get("/")

    @classmethod
    def tearDownClass(cls) -> None:
        os.system("rm -rf media/product_images/default*.jpg")
        super().tearDownClass()

    def test_serialization(self) -> None:
        serializer = VariantSerializer(
            self.variants[0], context={"request": self.request}
        )
        data = serializer.data
        fields = [
            "id",
            "created_at",
            "updated_at",
            "product",
            "size",
            "color",
            "image",
            "cost",
            "price",
            "quantity",
            "url",
            "wished_by",
            "sort_order",
        ]

        self.assertEqual(set(data.keys()), set(fields))
        self.assertEqual(data["product"], self.product.id)
        self.assertEqual(
            data["url"], f"http://testserver/api/variants/{self.variants[0].id}/"
        )
        self.assertEqual(data["wished_by"], 0)
        self.assertEqual(data["sort_order"], self.variants[0].sort_order)
        self.assertEqual(data["size"], self.variants[0].size.id)
        self.assertEqual(data["color"], self.variants[0].color.id)
        self.assertEqual(data["image"], self.variants[0].image.id)
        self.assertEqual(Decimal(data["cost"]), self.variants[0].cost)
        self.assertEqual(Decimal(data["price"]), self.variants[0].price)
        self.assertEqual(data["quantity"], self.variants[0].quantity)
        self.assertEqual(data["sort_order"], self.variants[0].sort_order)

    def test_serialization_many(self) -> None:
        serializer = VariantSerializer(
            self.variants, many=True, context={"request": self.request}
        )
        data = serializer.data
        self.assertEqual(len(data), 5)
        for variant, serialized in zip(self.variants, data):
            self.assertEqual(serialized["product"], variant.product.id)
            self.assertEqual(
                serialized["url"],
                f"http://testserver/api/variants/{variant.id}/",
            )
            self.assertEqual(serialized["wished_by"], 0)
            self.assertEqual(serialized["sort_order"], variant.sort_order)
            self.assertEqual(serialized["size"], variant.size.id)
            self.assertEqual(serialized["color"], variant.color.id)
            self.assertEqual(serialized["image"], variant.image.id)
            self.assertEqual(Decimal(serialized["cost"]), variant.cost)
            self.assertEqual(Decimal(serialized["price"]), variant.price)
            self.assertEqual(serialized["quantity"], variant.quantity)
            self.assertEqual(serialized["sort_order"], variant.sort_order)

    def test_create(self) -> None:
        size = Size.objects.first()
        color = ColorFactory()
        image = ImgFactory()
        data = {
            "product": self.product.id,
            "size": size.id,
            "color": color.id,
            "image": image.id,
            "cost": "10.00",
            "price": "20.00",
            "quantity": 10,
            "sort_order": 20,
        }
        serializer = VariantSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertSetEqual(
            set(serializer.validated_data.keys()),
            {
                "product",
                "size",
                "color",
                "image",
                "cost",
                "price",
                "quantity",
                "sort_order",
            },
        )
        variant = serializer.save()
        self.assertEqual(variant.product, self.product)
        self.assertEqual(variant.size, size)
        self.assertEqual(variant.color, color)
        self.assertEqual(variant.image, image)
        self.assertEqual(variant.cost, Decimal("10.00"))
        self.assertEqual(variant.price, Decimal("20.00"))
        self.assertEqual(variant.quantity, 10)
        self.assertEqual(variant.sort_order, 20)
        self.assertEqual(variant.wished_by.count(), 0)
        self.assertIsNotNone(variant.created_at)
        self.assertIsNotNone(variant.updated_at)

    def test_update(self) -> None:
        size = Size.objects.first()
        color = Color.objects.first()
        image = ImgFactory()
        variant = VariantFactory(product=self.product)
        data = {
            "product": self.product.id,
            "size": size.id,
            "color": color.id,
            "image": image.id,
            "cost": "10.00",
            "price": "20.00",
            "quantity": 10,
            "sort_order": 30,
        }
        serializer = VariantSerializer(variant, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertSetEqual(
            set(serializer.validated_data.keys()),
            {
                "product",
                "size",
                "color",
                "image",
                "cost",
                "price",
                "quantity",
                "sort_order",
            },
        )
        updated_variant = serializer.save()
        self.assertIs(variant, updated_variant)
        self.assertEqual(updated_variant.product, self.product)
        self.assertEqual(updated_variant.size, size)
        self.assertEqual(updated_variant.color, color)
        self.assertEqual(updated_variant.image, image)
        self.assertEqual(updated_variant.cost, Decimal("10.00"))
        self.assertEqual(updated_variant.price, Decimal("20.00"))
        self.assertEqual(updated_variant.quantity, 10)
        self.assertEqual(updated_variant.sort_order, 30)

    def test_update_partial(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"cost": "10.00", "price": "20.00"}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertSetEqual(set(serializer.validated_data.keys()), {"cost", "price"})
        updated_variant = serializer.save()
        self.assertIs(variant, updated_variant)
        self.assertEqual(updated_variant.cost, Decimal("10.00"))
        self.assertEqual(updated_variant.price, Decimal("20.00"))

    def test_update_partial_invalid_price(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"cost": "10.00", "price": "invalid"}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"price"})
        self.assertEqual(serializer.errors["price"][0].code, "invalid")
        self.assertEqual(
            str(serializer.errors["price"][0]), "A valid number is required."
        )

    def test_update_partial_invalide_cost(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"cost": "invalid", "price": "20.00"}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"cost"})
        self.assertEqual(serializer.errors["cost"][0].code, "invalid")
        self.assertEqual(
            str(serializer.errors["cost"][0]), "A valid number is required."
        )

    def test_update_partial_negative_cost(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"cost": "-10.00", "price": "20.00"}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"cost"})
        self.assertEqual(serializer.errors["cost"][0].code, "min_value")
        self.assertEqual(
            str(serializer.errors["cost"][0]),
            "Ensure this value is greater than or equal to 0.",
        )

    def test_update_partial_negative_price(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"cost": "10.00", "price": "-20.00"}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"price"})
        self.assertEqual(serializer.errors["price"][0].code, "min_value")
        self.assertEqual(
            str(serializer.errors["price"][0]),
            "Ensure this value is greater than or equal to 0.",
        )

    def test_required_fields(self) -> None:
        serializer = VariantSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(
            set(serializer.errors.keys()),
            {"product", "image", "cost", "price", "quantity"},
        )
        self.assertEqual(serializer.errors["product"][0].code, "required")
        self.assertEqual(serializer.errors["image"][0].code, "required")
        self.assertEqual(serializer.errors["cost"][0].code, "required")
        self.assertEqual(serializer.errors["price"][0].code, "required")
        self.assertEqual(serializer.errors["quantity"][0].code, "required")
        self.assertEqual(
            str(serializer.errors["product"][0]), "This field is required."
        )
        self.assertEqual(str(serializer.errors["image"][0]), "This field is required.")
        self.assertEqual(str(serializer.errors["cost"][0]), "This field is required.")
        self.assertEqual(str(serializer.errors["price"][0]), "This field is required.")
        self.assertEqual(
            str(serializer.errors["quantity"][0]), "This field is required."
        )

    def test_update_partial_invalid_product(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"product": 100}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"product"})
        self.assertEqual(serializer.errors["product"][0].code, "does_not_exist")
        self.assertEqual(
            str(serializer.errors["product"][0]),
            'Invalid pk "100" - object does not exist.',
        )

    def test_update_partial_invalid_size(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"size": 100}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"size"})
        self.assertEqual(serializer.errors["size"][0].code, "does_not_exist")
        self.assertEqual(
            str(serializer.errors["size"][0]),
            'Invalid pk "100" - object does not exist.',
        )

    def test_update_partial_invalid_color(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"color": 100}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"color"})
        self.assertEqual(serializer.errors["color"][0].code, "does_not_exist")
        self.assertEqual(
            str(serializer.errors["color"][0]),
            'Invalid pk "100" - object does not exist.',
        )

    def test_update_partial_invalid_image(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"image": 100}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"image"})
        self.assertEqual(serializer.errors["image"][0].code, "does_not_exist")
        self.assertEqual(
            str(serializer.errors["image"][0]),
            'Invalid pk "100" - object does not exist.',
        )

    def test_update_partial_invalid_sort_order(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"sort_order": -1}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"sort_order"})
        self.assertEqual(serializer.errors["sort_order"][0].code, "min_value")
        self.assertEqual(
            str(serializer.errors["sort_order"][0]),
            "Ensure this value is greater than or equal to 0.",
        )

    def test_update_partial_invalid_quantity(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"quantity": -1}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertSetEqual(set(serializer.errors.keys()), {"quantity"})
        self.assertEqual(serializer.errors["quantity"][0].code, "min_value")
        self.assertEqual(
            str(serializer.errors["quantity"][0]),
            "Ensure this value is greater than or equal to 0.",
        )

    def test_extra_fields(self) -> None:
        variant = VariantFactory(product=self.product)
        data = {"extra": "extra"}
        serializer = VariantSerializer(variant, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertSetEqual(set(serializer.validated_data.keys()), set())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.save(), variant)

    def test_extra_fields_create(self) -> None:
        size = Size.objects.first()
        color = Color.objects.first()
        image = ImgFactory()
        data = {
            "product": self.product.id,
            "size": size.id,
            "color": color.id,
            "image": image.id,
            "cost": "10.00",
            "price": "20.00",
            "quantity": 10,
            "sort_order": 40,
            "extra": "extra",
        }
        serializer = VariantSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertSetEqual(
            set(serializer.validated_data.keys()),
            {
                "product",
                "size",
                "color",
                "image",
                "cost",
                "price",
                "quantity",
                "sort_order",
            },
        )


class NestedVariantSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        SizeFactory.create_batch(5)
        cls.product = ProductFactory()
        cls.variants = VariantFactory.create_batch(5, product=cls.product)
        cls.request = RequestFactory().get("/")

    @classmethod
    def tearDownClass(cls) -> None:
        os.system("rm -rf media/product_images/default*.jpg")
        super().tearDownClass()

    def test_serialization(self) -> None:
        serializer = ProductDetailVariantSerializer(
            self.variants[0], context={"request": self.request}
        )
        data = serializer.data
        nested_size = {
            "id": str(self.variants[0].size.id),
            "name": self.variants[0].size.name,
        }
        nested_color = {
            "id": str(self.variants[0].color.id),
            "color1_name": self.variants[0].color.color1_name,
            "color1_value": self.variants[0].color.color1_value,
            "color2_name": self.variants[0].color.color2_name,
            "color2_value": self.variants[0].color.color2_value,
        }
        nested_img = {
            "id": str(self.variants[0].image.id),
            "src": self.request.build_absolute_uri(self.variants[0].image.src.url),
            "alt": self.variants[0].image.alt,
        }
        fields = [
            "id",
            "updated_at",
            "created_at",
            "size",
            "color",
            "image",
            "price",
            "cost",
            "sort_order",
            "quantity",
        ]

        self.assertEqual(set(data.keys()), set(fields))
        self.assertEqual(data["size"], nested_size)
        self.assertEqual(data["color"], nested_color)
        self.assertEqual(data["image"], nested_img)
        self.assertEqual(Decimal(data["price"]), self.variants[0].price)
        self.assertEqual(Decimal(data["cost"]), self.variants[0].cost)
        self.assertEqual(data["sort_order"], self.variants[0].sort_order)
        self.assertEqual(data["quantity"], self.variants[0].quantity)

    def test_serialization_many(self) -> None:
        serializer = ProductDetailVariantSerializer(
            self.variants, many=True, context={"request": self.request}
        )
        data = serializer.data
        self.assertEqual(len(data), 5)
        for variant, serialized in zip(self.variants, data):
            nested_size = {
                "id": str(variant.size.id),
                "name": variant.size.name,
            }
            nested_color = {
                "id": str(variant.color.id),
                "color1_name": variant.color.color1_name,
                "color1_value": variant.color.color1_value,
                "color2_name": variant.color.color2_name,
                "color2_value": variant.color.color2_value,
            }
            nested_img = {
                "id": str(variant.image.id),
                "src": self.request.build_absolute_uri(variant.image.src.url),
                "alt": variant.image.alt,
            }
            self.assertEqual(serialized["size"], nested_size)
            self.assertEqual(serialized["color"], nested_color)
            self.assertEqual(serialized["image"], nested_img)
            self.assertEqual(Decimal(serialized["price"]), variant.price)
            self.assertEqual(Decimal(serialized["cost"]), variant.cost)
            self.assertEqual(serialized["sort_order"], variant.sort_order)
            self.assertEqual(serialized["quantity"], variant.quantity)
            self.assertEqual(serialized["sort_order"], variant.sort_order)

    def test_all_fields_are_read_only(self) -> None:
        """Enusres that there is no deserialization (no create or update)"""
        data = {
            "size": {"id": 1, "name": "XS"},
            "color": {"id": 1, "color1_name": "Black", "color1_value": "#000000"},
            "image": {"id": 1, "src": "http://testserver/media/default.jpg", "alt": ""},
            "price": "10.00",
            "cost": "20.00",
            "sort_order": 1,
            "quantity": 10,
        }
        serializer = ProductDetailVariantSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
