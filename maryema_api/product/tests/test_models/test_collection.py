import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from product.models import Category, Collection, Division, Product


class CollectionModelTest(TestCase):
    """Test suite for Collection model"""

    def setUp(self) -> None:
        self.division = Division.objects.create(name="Test Division")
        self.category = Category.objects.create(
            division=self.division, name="Test Category"
        )
        self.product1 = Product.objects.create(
            name="Test Product1",
            description="Test Description 1",
            category=self.category,
        )
        self.product2 = Product.objects.create(
            name="Test Product2",
            description="Test Description 2",
            category=self.category,
        )
        self.product3 = Product.objects.create(
            name="Test Product2",
            description="Test Description 3",
            category=self.category,
        )

    def test_create_collection(self) -> None:
        """Test Collection creation"""
        collection = Collection.objects.create(
            name="Test Collection",
            description="Test Description",
        )
        collection.products.add(self.product1)
        collection.products.add(self.product2)
        collection.products.add(self.product3)
        self.assertEqual(collection.products.count(), 3)
        self.assertEqual(collection.name, "Test Collection")
        self.assertEqual(collection.description, "Test Description")

    def test_str_representation(self) -> None:
        """Test Collection string representation"""
        collection = Collection.objects.create(
            name="Test Collection",
            description="Test Description",
        )
        self.assertEqual(str(collection), "Test Collection")

    def test_required_name(self) -> None:
        """Test required name"""
        with self.assertRaises(ValidationError):
            Collection.objects.create(description="Test Description")

    def test_collection_inheritance_from_basemodel(self) -> None:
        """Test Collection inheritance from BaseModel"""
        collection = Collection.objects.create(
            name="Test Collection",
            description="Test Description",
        )
        self.assertTrue(hasattr(collection, "id"))
        self.assertTrue(isinstance(collection.id, uuid.UUID))
        self.assertTrue(hasattr(collection, "created_at"))
        self.assertTrue(isinstance(collection.created_at, datetime))
        self.assertTrue(hasattr(collection, "updated_at"))
        self.assertTrue(isinstance(collection.updated_at, datetime))

    def test_collection_with_empty_products_set(self) -> None:
        """Test Collection with empty products set"""
        collection = Collection.objects.create(
            name="Test Collection",
            description="Test Description",
        )
        self.assertEqual(collection.products.count(), 0)

    def test_collection_with_products(self) -> None:
        """Test Collection with products"""
        collection = Collection.objects.create(
            name="Test Collection",
            description="Test Description",
        )
        collection.products.set([self.product1, self.product2])
        self.assertEqual(collection.products.count(), 2)
        self.assertTrue(self.product1 in collection.products.all())
        self.assertTrue(self.product2 in collection.products.all())
        self.assertFalse(self.product3 in collection.products.all())

    def test_emptying_collection(self) -> None:
        """Test emptying collection"""
        collection = Collection.objects.create(
            name="Test Collection",
            description="Test Description",
        )
        collection.products.set([self.product1, self.product2])
        self.assertEqual(collection.products.count(), 2)
        collection.products.clear()
        self.assertEqual(collection.products.count(), 0)
        self.assertIsNotNone(self.product1)

    def test_deleting_product_in_collection_products_list(self) -> None:
        """Test deleting product in collection products list"""
        collection = Collection.objects.create(
            name="Test Collection",
            description="Test Description",
        )
        collection.products.set([self.product1, self.product2])
        self.assertEqual(collection.products.count(), 2)
        self.product1.delete()
        self.assertEqual(collection.products.count(), 1)
        self.assertFalse(self.product1 in collection.products.all())
        self.assertTrue(self.product2 in collection.products.all())
