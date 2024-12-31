import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.utils import create_image
from product.models import Img


class TestImgModel(TestCase):
    """A test suit for Img model"""

    def test_str(self) -> None:
        """Test string representation"""
        img = Img.objects.create(src=create_image(), alt="An image for product 1")
        self.assertEqual(str(img), "An image for product 1")

    def test_img_inheritance_from_basemodel(self) -> None:
        """Test that Img model inherit from BaseModel model"""
        image = Img.objects.create(src=create_image(), alt="An image for product 1")
        self.assertTrue(hasattr(image, "id"))
        self.assertTrue(isinstance(image.id, uuid.UUID))
        self.assertTrue(hasattr(image, "created_at"))
        self.assertTrue(isinstance(image.created_at, datetime))
        self.assertTrue(hasattr(image, "updated_at"))
        self.assertTrue(isinstance(image.updated_at, datetime))

    def test_src_is_required(self) -> None:
        """Test that src field is required"""
        with self.assertRaises(ValidationError):
            Img.objects.create(alt="An image for product 1")

    def test_alt_is_optional(self) -> None:
        """Test that alt field is optional"""
        img = Img.objects.create(src=create_image())
        self.assertEqual(img.alt, "")
