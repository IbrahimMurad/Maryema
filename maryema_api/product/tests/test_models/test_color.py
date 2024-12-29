import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from product.models import Color


class TestColorModel(TestCase):
    """Test suite for Color model"""

    def test_str(self) -> None:
        """Test string representation"""
        color1 = Color.objects.create(color1_name="red", color1_value="#ff0000")
        self.assertEqual(str(color1), "red")
        color2 = Color.objects.create(
            color1_name="red",
            color1_value="#ff0000",
            color2_name="blue",
            color2_value="#0000ff",
        )
        self.assertEqual(str(color2), "red-blue")

    def test_color_inheritance_from_basemodel(self) -> None:
        """Test that Color model inherit from BaseModel model"""
        color = Color.objects.create(color1_name="red", color1_value="#ff0000")
        self.assertTrue(hasattr(color, "id"))
        self.assertTrue(isinstance(color.id, uuid.UUID))
        self.assertTrue(hasattr(color, "created_at"))
        self.assertTrue(isinstance(color.created_at, datetime))
        self.assertTrue(hasattr(color, "updated_at"))
        self.assertTrue(isinstance(color.updated_at, datetime))

    def test_color1_name_is_required(self) -> None:
        """Test that color1_name field is required"""
        with self.assertRaises(ValidationError):
            Color.objects.create(color1_value="#ff0000")

    def test_color1_value_is_optional(self) -> None:
        """Test that color1_value field is required"""
        color = Color.objects.create(color1_name="red")
        self.assertIsNone(color.color1_value)

    def test_color2_name_is_optional(self) -> None:
        """Test that color2_name field is optional"""
        color = Color.objects.create(color1_name="red", color1_value="#ff0000")
        self.assertIsNone(color.color2_name)

    def test_color2_value_is_optional(self) -> None:
        """Test that color2_value field is optional"""
        color = Color.objects.create(color1_name="red", color1_value="#ff0000")
        self.assertIsNone(color.color2_value)

    def test_color1_value_is_Invalid(self) -> None:
        """Test that color1_value field is a valid color"""
        with self.assertRaises(ValueError):
            Color.objects.create(color1_name="red", color1_value="ff0000")
        with self.assertRaises(ValueError):
            Color.objects.create(color1_name="red", color1_value="#gg000")
        with self.assertRaises(ValueError):
            Color.objects.create(color1_name="red", color1_value="#ff00000")
        with self.assertRaises(ValueError):
            Color.objects.create(color1_name="red", color1_value="#ff")

    def test_color2_value_is_Invalid(self) -> None:
        """Test that color2_value field is a valid color"""
        with self.assertRaises(ValueError):
            Color.objects.create(
                color1_name="red", color1_value="#ff0000", color2_value="ff0000"
            )
