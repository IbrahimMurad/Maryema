from profile.tests.factories import ProfileFactory

from django.test import RequestFactory, TestCase

from product.serializers import ProductSerializer
from product.tests.factories import CategoryFactory, ProductFactory


class TestProductSerializer(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.products = ProductFactory.create_batch(10)
        cls.product = cls.products[0]
        cls.request = RequestFactory().get("/")
        cls.product_serializer = ProductSerializer(
            cls.product, context={"request": cls.request}
        )

    def test_product_serialization(self) -> None:
        data = self.product_serializer.data
        self.assertIn("id", data)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)
        self.assertEqual(data["name"], self.product.name)
        self.assertEqual(data["description"], self.product.description)
        self.assertEqual(
            data["url"],
            self.request.build_absolute_uri(f"api/products/{self.product.id}/"),
        )
        self.assertIsNone(data["provider"])
        self.assertEqual(
            data["feedback"],
            self.request.build_absolute_uri(
                f"api/products/{self.product.id}/feedback/"
            ),
        )

    def test_product_serialization_many(self) -> None:
        products_serializer = ProductSerializer(
            self.products, many=True, context={"request": self.request}
        )
        data = products_serializer.data
        self.assertEqual(len(data), 10)
        for product_data, product in zip(data, self.products):
            self.assertIn("id", product_data)
            self.assertIn("created_at", product_data)
            self.assertIn("updated_at", product_data)
            self.assertEqual(product_data["name"], product.name)
            self.assertEqual(product_data["description"], product.description)
            self.assertEqual(
                product_data["url"],
                self.request.build_absolute_uri(f"api/products/{product.id}/"),
            )
            self.assertIsNone(product_data["provider"])
            self.assertEqual(
                product_data["feedback"],
                self.request.build_absolute_uri(f"api/products/{product.id}/feedback/"),
            )

    def test_product_valid_create(self) -> None:
        category = CategoryFactory()
        data = {
            "name": "Product Test",
            "description": "Product Description",
            "category": category.id,
            "tags": "tag1,tag2",
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.name, "Product Test")
        self.assertEqual(product.description, "Product Description")
        self.assertEqual(product.category, category)
        self.assertEqual(product.tags, "tag1,tag2")

    def test_product_valid_update(self) -> None:
        category = CategoryFactory()
        data = {
            "name": "Product Test",
            "description": "Product Description",
            "category": category.id,
            "tags": "tag1,tag2",
        }
        serializer = ProductSerializer(self.product, data=data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.name, "Product Test")
        self.assertEqual(product.description, "Product Description")
        self.assertEqual(product.category, category)
        self.assertEqual(product.tags, "tag1,tag2")

    def test_product_valid_partial_update(self) -> None:
        data = {
            "description": "New Description",
        }
        old_name = self.product.name
        old_category = self.product.category
        old_tags = self.product.tags
        serializer = ProductSerializer(self.product, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)
        product = serializer.save()
        self.assertEqual(product.name, old_name)
        self.assertEqual(product.description, "New Description")
        self.assertEqual(product.category, old_category)
        self.assertEqual(product.tags, old_tags)

    def test_product_create_with_missing_required_field(self) -> None:
        data = {
            "name": "Product Test",
            "description": "Product Description",
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)
        self.assertEqual(serializer.errors["category"][0].code, "required")

    def test_product_create_with_invalid_provider(self) -> None:
        provider = ProfileFactory()  # This is a customer
        data = {
            "name": "Product Test",
            "description": "Product Description",
            "category": CategoryFactory().id,
            "provider": provider.id,
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("provider", serializer.errors)
        print(serializer.errors)
        self.assertEqual(serializer.errors["provider"][0].code, "invalid")
        self.assertEqual(
            str(serializer.errors["provider"][0]),
            "Only providers can provide products",
        )

    def test_product_read_only_fileds(self) -> None:
        data = {
            "id": "1",
            "name": "Product Test",
            "description": "Product Description",
            "category": CategoryFactory().id,
            "tags": "tag1,tag2",
        }
        serializer = ProductSerializer(self.product, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("id", serializer.validated_data)
        product = serializer.save()
        self.assertNotEqual(product.id, 1)
        self.assertEqual(product.name, "Product Test")
        self.assertEqual(product.description, "Product Description")
        self.assertEqual(product.tags, "tag1,tag2")

    def test_create_product_with_extra_fileds(self) -> None:
        data = {
            "name": "Product Test",
            "description": "Product Description",
            "category": CategoryFactory().id,
            "tags": "tag1,tag2",
            "extra": "extra",
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("extra", serializer.validated_data)
        product = serializer.save()
        self.assertEqual(product.name, "Product Test")
        self.assertEqual(product.description, "Product Description")
        self.assertEqual(product.tags, "tag1,tag2")
        with self.assertRaises(AttributeError):
            product.extra
