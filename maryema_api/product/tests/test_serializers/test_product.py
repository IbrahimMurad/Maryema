import os
from profile.tests.factories import ProfileFactory

from django.db.models import Sum
from django.test import RequestFactory, TestCase

from product.serializers import (
    ProductDetailPublicSerializer,
    ProductListPublicSerializer,
    ProductSerializer,
)
from product.tests.factories import (
    CategoryFactory,
    ProductFactory,
    SizeFactory,
    VariantFactory,
)


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


class ProductPublicSerializerTestCase(TestCase):
    """
    A test suit for ProductDetailPublicSerializer and ProductListPublicSerializer
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.products = ProductFactory.create_batch(10)
        cls.request = RequestFactory().get("/")
        SizeFactory.create_batch(6)

        # create suffecient variants for each product and reset the squence each time
        # to start sort_order field for the variants of each product from 1
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(12, product=cls.products[0])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(12, product=cls.products[1])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(10, product=cls.products[2])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(7, product=cls.products[3])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(5, product=cls.products[4])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(1, product=cls.products[5])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(3, product=cls.products[6])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(2, product=cls.products[7])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(9, product=cls.products[8])
        VariantFactory.reset_sequence(1)
        VariantFactory.create_batch(9, product=cls.products[9])
        cls.serialized_products = ProductListPublicSerializer(
            cls.products, many=True, context={"request": cls.request}
        ).data
        cls.serialized_product = ProductDetailPublicSerializer(
            cls.products[0], context={"request": cls.request}
        ).data

    @classmethod
    def tearDownClass(cls) -> None:
        VariantFactory.reset_sequence(1)
        os.system("rm -rf media/product_images/default*.jpg")
        super().tearDownClass()

    def test_product_list_public_serialization(self) -> None:
        self.assertEqual(len(self.serialized_products), 10)
        for product_data, product in zip(self.serialized_products, self.products):
            self.assertIn("id", product_data)
            self.assertIn("created_at", product_data)
            self.assertIn("updated_at", product_data)
            self.assertEqual(product_data["name"], product.name)
            self.assertEqual(product_data["description"], product.description)
            self.assertEqual(
                product_data["url"],
                self.request.build_absolute_uri(f"api/products/{product.id}/"),
            )
            self.assertEqual(
                product_data["feedback"],
                self.request.build_absolute_uri(f"api/products/{product.id}/feedback/"),
            )
            self.assertIn("image", product_data)
            self.assertIn("price", product_data)
            self.assertIn("in_stock", product_data)
            self.assertEqual(
                product_data["in_stock"],
                product.variants.all().aggregate(in_stock=Sum("quantity"))["in_stock"],
            )
            self.assertEqual(
                product_data["price"], product.variants.get(sort_order=1).price
            )
            self.assertEqual(
                product_data["image"], product.variants.get(sort_order=1).image.src.url
            )

    def test_product_list_public_deserialization(self) -> None:
        """Ensures this serializer is read only (no deserialization)"""
        data = {
            "id": "1",
            "name": "Product Test",
            "description": "Product Description",
            "category": CategoryFactory().id,
            "tags": "tag1,tag2",
            "extra": "extra",
        }
        serializer = ProductListPublicSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})

    def test_product_detail_public_serialization(self) -> None:
        fields = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "tags",
            "description",
            "category",
            "feedbacks",
            "variants",
        ]
        self.assertEqual(set(self.serialized_product.keys()), set(fields))
        self.assertEqual(len(self.serialized_product["variants"]), 12)
        # may add more assertions for variants fields after creating the test for its serializer

    def test_product_detail_public_deserialization(self) -> None:
        """Ensures this serializer is read only (no deserialization)"""
        data = {
            "id": "1",
            "name": "Product Test",
            "description": "Product Description",
            "category": CategoryFactory().id,
            "tags": "tag1,tag2",
            "extra": "extra",
        }
        serializer = ProductDetailPublicSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
