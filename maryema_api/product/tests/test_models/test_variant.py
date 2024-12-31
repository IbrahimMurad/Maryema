import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import deletion
from django.test import TestCase

from core.utils import create_image
from product.models import Category, Color, Division, Img, Product, ProductVariant, Size


class TestProductVariantModel(TestCase):
    """A test suit for ProductVariant model"""

    def setUp(self) -> None:
        self.division = Division.objects.create(name="Clothing")
        self.category = Category.objects.create(name="T-shirts", division=self.division)
        self.color = Color.objects.create(color1_name="Red")
        self.size = Size.objects.create(name="XL")
        self.product = Product.objects.create(category=self.category, name="T-shirt 1")
        self.image = Img.objects.create(
            src=create_image(), alt="An image for product 1"
        )

    def test_str(self) -> None:
        """Test string representation"""
        variant = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        self.assertEqual(str(variant), "T-shirt 1 - Red - XL")

    def test_create_product_variant(self) -> None:
        """Test creating a product variant"""
        variant = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        self.assertEqual(variant.product, self.product)
        self.assertEqual(variant.color, self.color)
        self.assertEqual(variant.size, self.size)
        self.assertEqual(variant.image, self.image)
        self.assertEqual(variant.cost, 10.0)
        self.assertEqual(variant.price, 20.0)
        self.assertEqual(variant.quantity, 10)
        self.assertEqual(variant.sort_order, 1)

    def test_preoduct_is_required(self) -> None:
        """Test product is required"""
        with self.assertRaises(ValidationError):
            ProductVariant.objects.create(
                color=self.color,
                size=self.size,
                image=self.image,
                cost=10.0,
                price=20.0,
                quantity=10,
            )

    def test_image_is_required(self) -> None:
        """Test image is required"""
        with self.assertRaises(ValidationError):
            ProductVariant.objects.create(
                product=self.product,
                color=self.color,
                size=self.size,
                cost=10.0,
                price=20.0,
                quantity=10,
            )

    def test_cost_is_required(self) -> None:
        """Test cost is required"""
        with self.assertRaises(ValidationError):
            ProductVariant.objects.create(
                product=self.product,
                color=self.color,
                size=self.size,
                image=self.image,
                price=20.0,
                quantity=10,
            )

    def test_price_is_required(self) -> None:
        """Test price is required"""
        with self.assertRaises(ValidationError):
            ProductVariant.objects.create(
                product=self.product,
                color=self.color,
                size=self.size,
                image=self.image,
                cost=10.0,
                quantity=10,
            )

    def test_quantity_is_reuqired(self) -> None:
        """Test quantity is required"""
        with self.assertRaises(ValidationError):
            ProductVariant.objects.create(
                product=self.product,
                color=self.color,
                size=self.size,
                image=self.image,
                cost=10.0,
                price=20.0,
            )

    def test_price_greater_than_cost(self) -> None:
        """Test price is greater than cost"""
        with self.assertRaises(ValueError):
            ProductVariant.objects.create(
                product=self.product,
                color=self.color,
                size=self.size,
                image=self.image,
                cost=20.0,
                price=10.0,
                quantity=10,
            )

    def test_product_variant_inheritance_from_base_model(self) -> None:
        """Test ProductVariant inherits BaseModel"""
        variant = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        self.assertTrue(hasattr(variant, "id"))
        self.assertIsInstance(variant.id, uuid.UUID)
        self.assertTrue(hasattr(variant, "created_at"))
        self.assertIsInstance(variant.created_at, datetime)
        self.assertTrue(hasattr(variant, "updated_at"))
        self.assertIsInstance(variant.updated_at, datetime)

    def test_product_variants_relation(self) -> None:
        """Test the relation between Product model and ProductVariant model"""
        size1 = Size.objects.create(name="S")
        size2 = Size.objects.create(name="M")
        color1 = Color.objects.create(color1_name="Green")
        color2 = Color.objects.create(color1_name="Blue")
        image1 = Img.objects.create(src=create_image(name="image1.png"), alt="Image 1")
        image2 = Img.objects.create(src=create_image(name="image2.png"), alt="Image 2")
        variant1 = ProductVariant.objects.create(
            product=self.product,
            color=color1,
            size=size1,
            image=image1,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        variant2 = ProductVariant.objects.create(
            product=self.product,
            color=color1,
            size=size2,
            image=image1,
            cost=15.0,
            price=25.0,
            quantity=15,
            sort_order=2,
        )
        variant3 = ProductVariant.objects.create(
            product=self.product,
            color=color2,
            size=size1,
            image=image2,
            cost=12.0,
            price=22.0,
            quantity=10,
            sort_order=3,
        )
        variant4 = ProductVariant.objects.create(
            product=self.product,
            color=color2,
            size=size2,
            image=image2,
            cost=18.0,
            price=30.0,
            quantity=15,
            sort_order=4,
        )
        self.assertEqual(self.product.variants.count(), 4)
        self.assertIn(variant1, self.product.variants.all())
        self.assertIn(variant2, self.product.variants.all())
        self.assertIn(variant3, self.product.variants.all())
        self.assertIn(variant4, self.product.variants.all())
        self.assertEqual(variant1.product, self.product)
        self.assertEqual(variant2.product, self.product)
        self.assertEqual(variant3.product, self.product)
        self.assertEqual(variant4.product, self.product)
        self.product.delete()
        self.assertEqual(ProductVariant.objects.all().count(), 0)

    def test_variant_color_relation(self) -> None:
        """Test the relation between Color model and ProductVariant model"""
        variant = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        self.assertEqual(self.color.variants.count(), 1)
        self.assertIn(variant, self.color.variants.all())
        self.assertEqual(variant.color, self.color)
        self.color.delete()
        self.assertEqual(ProductVariant.objects.all().count(), 1)
        variant.refresh_from_db()
        self.assertIsNotNone(variant)
        self.assertIsNone(variant.color)

    def test_variant_size_relation(self) -> None:
        """Test the relation between Size model and ProductVariant model"""
        variant = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        self.assertEqual(self.size.variants.count(), 1)
        self.assertIn(variant, self.size.variants.all())
        self.assertEqual(variant.size, self.size)
        self.size.delete()
        self.assertEqual(ProductVariant.objects.all().count(), 1)
        variant.refresh_from_db()
        self.assertIsNotNone(variant)
        self.assertIsNone(variant.size)

    def test_variant_image_relation(self) -> None:
        """Test the relation between Img model and ProductVariant model"""
        variant = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        self.assertEqual(self.image.variants.count(), 1)
        self.assertIn(variant, self.image.variants.all())
        self.assertEqual(variant.image, self.image)

    def test_variant_image_deletion(self) -> None:
        """Test the deletion of an image"""
        variant = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        with self.assertRaises(deletion.ProtectedError):
            self.image.delete()
        variant.delete()
        self.image.refresh_from_db()
        self.assertEqual(self.image.variants.count(), 0)
        self.image.delete()
        self.assertEqual(Img.objects.all().count(), 0)
        self.assertEqual(ProductVariant.objects.all().count(), 0)

    def test_variants_default_ordering(self) -> None:
        """Test default ordering of ProductVariant model"""
        size1 = Size.objects.create(name="S")
        size2 = Size.objects.create(name="M")
        color1 = Color.objects.create(color1_name="Green")
        color2 = Color.objects.create(color1_name="Blue")
        image1 = Img.objects.create(src=create_image(name="image1.png"), alt="Image 1")
        image2 = Img.objects.create(src=create_image(name="image2.png"), alt="Image 2")
        variant1 = ProductVariant.objects.create(
            product=self.product,
            color=color1,
            size=size1,
            image=image1,
            cost=10.0,
            price=20.0,
            quantity=10,
            sort_order=1,
        )
        variant2 = ProductVariant.objects.create(
            product=self.product,
            color=color1,
            size=size2,
            image=image1,
            cost=15.0,
            price=25.0,
            quantity=15,
            sort_order=2,
        )
        variant3 = ProductVariant.objects.create(
            product=self.product,
            color=color2,
            size=size1,
            image=image2,
            cost=12.0,
            price=22.0,
            quantity=10,
            sort_order=3,
        )
        variant4 = ProductVariant.objects.create(
            product=self.product,
            color=color2,
            size=size2,
            image=image2,
            cost=18.0,
            price=30.0,
            quantity=15,
            sort_order=4,
        )
        self.assertEqual(
            list(ProductVariant.objects.all()), [variant1, variant2, variant3, variant4]
        )

    def test_a_variant_is_unique_for_product_color_and_size(self) -> None:
        """Test a variant is unique for product, color, and size"""
        ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        with self.assertRaises(ValidationError):
            ProductVariant.objects.create(
                product=self.product,
                color=self.color,
                size=self.size,
                image=self.image,
                cost=10.0,
                price=20.0,
                quantity=10,
            )

    def test_sort_order_is_unique_for_product(self) -> None:
        """Test sort order is unique for product"""
        ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size,
            image=self.image,
            cost=10.0,
            price=20.0,
            quantity=10,
        )
        with self.assertRaises(ValidationError):
            ProductVariant.objects.create(
                product=self.product,
                color=self.color,
                size=self.size,
                image=self.image,
                cost=10.0,
                price=20.0,
                quantity=10,
            )
