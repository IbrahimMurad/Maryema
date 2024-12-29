import uuid
from datetime import datetime
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from product.models import Img


def create_image(
    name: str = "default.png", size: tuple[int, int] = (100, 100)
) -> SimpleUploadedFile:
    file: BytesIO = BytesIO()
    image: Image.Image = Image.new("RGB", size=size)
    image.save(file, "png")
    file.name = name
    file.seek(0)
    return SimpleUploadedFile(
        name=file.name, content=file.read(), content_type="image/png"
    )


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
