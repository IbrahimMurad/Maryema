import os

from django.test import TestCase
from django.test.client import RequestFactory

from core.utils import create_image
from product.models import Img
from product.serializers import ImgSerializer
from product.serializers.image import NestedImgSerializer
from product.tests.factories import ImgFactory


class ImgSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.image = ImgFactory.create()
        cls.request = RequestFactory().get("/")
        cls.serializer = ImgSerializer(
            instance=cls.image, context={"request": cls.request}
        )

    @classmethod
    def tearDownClass(cls) -> None:
        os.system("rm -rf media/product_images/default*")
        super().tearDownClass()

    def test_contains_expected_fields(self) -> None:
        data = self.serializer.data
        expected_fields = {"id", "url", "src", "alt", "created_at", "updated_at"}
        self.assertEqual(set(data.keys()), expected_fields)

    def test_serialization_many(self) -> None:
        ImgFactory.create_batch(3)
        serializer = ImgSerializer(
            Img.objects.all(), many=True, context={"request": self.request}
        )
        self.assertEqual(len(serializer.data), 4)
        expected_fields = {"id", "url", "src", "alt", "created_at", "updated_at"}
        for data in serializer.data:
            self.assertEqual(set(data.keys()), expected_fields)

    def test_url_field_uses_view_name(self) -> None:
        data = self.serializer.data
        self.assertTrue("url" in data)
        self.assertTrue(data["url"].endswith(f"/api/imgs/{self.image.id}/"))

    def test_alt_field_content(self) -> None:
        data = self.serializer.data
        self.assertEqual(data["alt"], self.image.alt)

    def test_create_with_valid_data(self) -> None:
        image_file = create_image()
        data = {"src": image_file, "alt": "Test Image"}

        serializer = ImgSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.validated_data, data)
        instance = serializer.save()
        self.assertIsInstance(instance, Img)
        self.assertEqual(instance.alt, "Test Image")

    def test_update_with_valid_data(self) -> None:
        image = Img.objects.get(id=self.image.id)
        new_data = {
            "src": create_image(name="new-image.jpg"),
            "alt": "Updated Image Alt",
        }

        serializer = ImgSerializer(instance=image, data=new_data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(set(serializer.validated_data.keys()), {"src", "alt"})
        updated_image = serializer.save()
        self.assertEqual(updated_image.alt, "Updated Image Alt")

    def test_partial_update_with_valid_data(self) -> None:
        image = Img.objects.get(id=self.image.id)
        new_data = {"alt": "Updated Image Alt"}

        serializer = ImgSerializer(instance=image, data=new_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_image = serializer.save()
        self.assertEqual(updated_image.alt, "Updated Image Alt")

    def test_create_with_invalid_data(self) -> None:
        data = {"src": "invalid-image-file", "alt": "Test Image"}

        serializer = ImgSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["src"][0]),
            "The submitted data was not a file. Check the encoding type on the form.",
        )

    def test_update_with_invalid_data(self) -> None:
        image = Img.objects.get(id=self.image.id)
        new_data = {"src": "invalid-image-file", "alt": "Updated Image Alt"}

        serializer = ImgSerializer(instance=image, data=new_data, partial=True)
        self.assertFalse(serializer.is_valid())
        print(serializer.errors)
        self.assertEqual(
            str(serializer.errors["src"][0]),
            "The submitted data was not a file. Check the encoding type on the form.",
        )


class NestedImgSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.image = ImgFactory.create()
        cls.serializer = NestedImgSerializer(instance=cls.image)

    def test_contains_expected_fields(self) -> None:
        data = self.serializer.data
        expected_fields = {"id", "src", "alt"}
        self.assertEqual(set(data.keys()), expected_fields)

    def test_serialization_many(self) -> None:
        ImgFactory.create_batch(3)
        serializer = NestedImgSerializer(Img.objects.all(), many=True)
        self.assertEqual(len(serializer.data), 4)
        expected_fields = {"id", "src", "alt"}
        for data in serializer.data:
            self.assertEqual(set(data.keys()), expected_fields)

    def test_excluded_fields(self) -> None:
        data = self.serializer.data
        excluded_fields = {"created_at", "updated_at"}
        self.assertEqual(set(data.keys()).intersection(excluded_fields), set())

    def test_read_only_fields(self) -> None:
        image = Img.objects.get(id=self.image.id)
        new_data = {"id": 999, "src": "new/path/to/image.jpg", "alt": "New Alt Text"}

        serializer = NestedImgSerializer(instance=image, data=new_data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        updated_image = serializer.save()

        self.assertNotEqual(updated_image.id, new_data["id"])
        self.assertNotEqual(str(updated_image.src), new_data["src"])
        self.assertNotEqual(updated_image.alt, new_data["alt"])
