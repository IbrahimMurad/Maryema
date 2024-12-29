import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from product.models import Size


class TestSizeModel(TestCase):
    """A test case for Size model"""

    def test_str(self) -> None:
        """Test string representation"""
        size = Size.objects.create(name="XL")
        self.assertEqual(str(size), "XL")

    def test_required_name(self) -> None:
        """test required name field (not null and not blank)"""
        size = Size()
        with self.assertRaises(ValidationError):
            size.save()
        size = Size(name="")
        with self.assertRaises(ValidationError):
            size.save()

    def test_size_inheritance_from_BaseModel(self) -> None:
        """Ensure Size model inherit from BaseModel"""
        size = Size.objects.create(name="XXL")
        self.assertIsNotNone(size.id)
        self.assertTrue(isinstance(size.id, uuid.UUID))
        self.assertIsNotNone(size.created_at)
        self.assertTrue(isinstance(size.created_at, datetime))
        self.assertIsNotNone(size.updated_at)
        self.assertTrue(isinstance(size.updated_at, datetime))

    def test_invalid_size(self) -> None:
        """Test invalid size"""
        with self.assertRaises(ValueError):
            Size.objects.create(name="Invalid Size")

    def test_valide_sizes(self) -> None:
        """Test valid size"""
        size = Size.objects.create(name="XL")
        self.assertEqual(size.name, "XL")
        size = Size.objects.create(name="S")
        self.assertEqual(size.name, "S")
        size = Size.objects.create(name="M")
        self.assertEqual(size.name, "M")
        size = Size.objects.create(name="L")
        self.assertEqual(size.name, "L")
        size = Size.objects.create(name="XS")
        self.assertEqual(size.name, "XS")
        size = Size.objects.create(name="XXL")
        self.assertEqual(size.name, "XXL")
        size = Size.objects.create(name="6")
        self.assertEqual(size.name, "6")
        size = Size.objects.create(name="28")
        self.assertEqual(size.name, "28")
