from django.test import RequestFactory, TestCase

from product.models import Size
from product.serializers.size import NestedSizeSerializer, SizeSerializer


class TestSizeSerializer(TestCase):
    """A test suit for SizeSerializer"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.request = RequestFactory().request()

    def test_size_serializer(self) -> None:
        size = Size.objects.create(name="XL")
        serializer = SizeSerializer(size, context={"request": self.request})
        self.assertEqual(serializer.data["name"], "XL")
        self.assertEqual(
            serializer.data["url"], f"http://testserver/api/sizes/{size.id}/"
        )
        self.assertIn("id", serializer.data)
        self.assertIn("created_at", serializer.data)
        self.assertIn("updated_at", serializer.data)

    def test_size_deserialization(self) -> None:
        data = {"name": "XL"}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        self.assertIn("name", serializer.validated_data)
        size = serializer.save()
        self.assertEqual(size.name, "XL")
        self.assertIsInstance(size, Size)

    def test_serialization_many(self) -> None:
        size1 = Size.objects.create(name="XL")
        size2 = Size.objects.create(name="L")
        serializer = SizeSerializer(
            Size.objects.all().order_by("name"),
            many=True,
            context={"request": self.request},
        )
        expected_url1 = f"http://testserver/api/sizes/{size1.id}/"
        expected_url2 = f"http://testserver/api/sizes/{size2.id}/"
        for size in serializer.data:
            if size["name"] == "XL":
                self.assertEqual(size["url"], expected_url1)
            else:
                self.assertEqual(size["url"], expected_url2)
            self.assertIn("id", size)
            self.assertIn("created_at", size)
            self.assertIn("updated_at", size)

    def test_update(self) -> None:
        size = Size.objects.create(name="XL")
        data = {"name": "L"}
        serializer = SizeSerializer(size, data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        size = serializer.save()
        self.assertEqual(size.name, "L")
        names = Size.objects.values_list("name", flat=True)
        self.assertNotIn("XL", names)
        self.assertIn("L", names)

    def test_missing_required_field(self) -> None:
        data = {}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "required")

    def test_size_name_is_not_valide(self) -> None:
        """Tests that the size name in [XS, S, M, L, XL, XXL, or any non-negative integer]"""
        data = {"name": "XXXL"}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "invalid_size")

        data = {"name": "1"}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())

        data = {"name": "Large"}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "invalid_size")

    def test_unique_field(self) -> None:
        Size.objects.create(name="XL")
        data = {"name": "XL"}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "unique")

    def test_extra_field(self) -> None:
        data = {"name": "XL", "extra": "extra"}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        self.assertIn("name", serializer.validated_data)
        self.assertNotIn("extra", serializer.validated_data)

    def test_serializer_run_validation(self) -> None:
        data = {"name": "  xl "}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(serializer.validated_data["name"], "XL")

        data = {"name": "x  l"}
        serializer = SizeSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "unique")

    def test_read_only_field(self) -> None:
        size = Size.objects.create(name="XL")
        data = {"id": "1", "name": "L"}
        serializer = SizeSerializer(size, data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        self.assertIn("name", serializer.validated_data)
        self.assertNotIn("id", serializer.validated_data)


class TestNestedSizeSerializer(TestCase):
    """A test suit for NestedSizeSerializer"""

    def test_nested_size_serializer(self) -> None:
        size = Size.objects.create(name="XL")
        serializer = NestedSizeSerializer(size)
        self.assertDictEqual(serializer.data, {"id": str(size.id), "name": "XL"})
        self.assertNotIn("url", serializer.data)
        self.assertNotIn("created_at", serializer.data)
        self.assertNotIn("updated_at", serializer.data)

    def test_no_deserialization(self) -> None:
        """Test that the NestedSizeSerializer does not support deserialization (no cteate or update)"""
        data = {"name": "XL"}
        serializer = NestedSizeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})

    def test_serialization_many(self) -> None:
        size1 = Size.objects.create(name="XL")
        size2 = Size.objects.create(name="L")
        serializer = NestedSizeSerializer(
            Size.objects.all().order_by("name"), many=True
        )
        for size in serializer.data:
            if size["name"] == "XL":
                self.assertEqual(size["id"], str(size1.id))
            else:
                self.assertEqual(size["id"], str(size2.id))

    def test_read_only_field(self) -> None:
        size = Size.objects.create(name="XL")
        data = {"id": "1", "name": "L"}
        serializer = NestedSizeSerializer(size, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("name", serializer.validated_data)
