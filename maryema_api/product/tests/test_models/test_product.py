import uuid
from datetime import datetime
from profile.models import Profile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from product.models import Category, Division, Product


class ProductModelTest(TestCase):
    """A test suit for Product model"""

    def setUp(self) -> None:
        """setup test data"""
        self.division = Division.objects.create(name="test division")
        self.category = Category.objects.create(
            division=self.division, name="test category"
        )
        self.user = User.objects.create_user(
            username="test_user",
            email="user@test.com",
            password="test_password",
        )
        self.provider = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.PROVIDER
        )

    def test_product_creation(self) -> None:
        """Test product creation"""
        product = Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
        )
        self.assertEqual(product.name, "test product")
        self.assertEqual(product.description, "test description")
        self.assertEqual(product.provider, self.provider)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.tags, "")

    def test_str_representation(self) -> None:
        """Test string representation"""
        product = Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
        )
        self.assertEqual(str(product), "test product")

    def test_product_creation_with_tags(self) -> None:
        """Test product creation with tags"""
        product = Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
            tags="tag1, tag2, tag3",
        )
        self.assertEqual(product.tags, "tag1, tag2, tag3")

    def test_product_search_by_tag(self) -> None:
        """Test product search by tag"""
        product = Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
            tags="tag1, tag2, tag3",
        )
        self.assertEqual(Product.objects.filter(tags__contains="tag1").count(), 1)
        self.assertEqual(Product.objects.filter(tags__contains="tag2").first(), product)

    def test_product_inheritance_from_basemodel(self) -> None:
        """Test product inheritance from BaseModel"""
        product = Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
        )
        self.assertIsNotNone(product.id)
        self.assertIsInstance(product.id, uuid.UUID)
        self.assertIsNotNone(product.created_at)
        self.assertIsInstance(product.created_at, datetime)
        self.assertIsNotNone(product.updated_at)
        self.assertIsInstance(product.updated_at, datetime)

    def test_required_category(self) -> None:
        """Test required category"""
        with self.assertRaises(ValidationError):
            Product.objects.create(
                name="test product",
                description="test description",
                provider=self.provider,
            )

    def test_required_name(self) -> None:
        """Test required name"""
        with self.assertRaises(ValidationError):
            Product.objects.create(
                category=self.category,
                description="test description",
                provider=self.provider,
            )

    def test_provider_must_be_provider_role(self) -> None:
        """Test provider profile has role equal to provider"""
        user = User.objects.create_user(
            username="test_user2", password="test_password", email="user2@test.com"
        )
        profile = Profile.objects.create(user=user, role=Profile.RoleChoices.CUSTOMER)
        with self.assertRaises(ValidationError):
            Product.objects.create(
                category=self.category,
                name="test product",
                description="test description",
                provider=profile,
            )

    def test_product_provider_relation(self) -> None:
        """Test product-provider relationship"""
        product = Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
        )
        self.assertEqual(product.provider, self.provider)
        self.assertEqual(self.provider.products.count(), 1)
        self.assertEqual(self.provider.products.first(), product)

    def test_product_category_relation(self) -> None:
        """Test product-category relationship"""
        product = Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
        )
        self.assertEqual(product.category, self.category)
        self.assertEqual(self.category.products.count(), 1)
        self.assertEqual(self.category.products.first(), product)

    def test_product_category_deletion(self) -> None:
        """Test product deletion when category is deleted"""
        Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
        )
        self.category.delete()
        self.assertEqual(Product.objects.count(), 0)

    def test_product_provider_deletion(self) -> None:
        """Test product deletion when provider is deleted"""
        product = Product.objects.create(
            category=self.category,
            name="test product",
            description="test description",
            provider=self.provider,
        )
        self.provider.delete()
        product.refresh_from_db()
        self.assertEqual(Product.objects.count(), 1)
        self.assertIsNone(product.provider)
