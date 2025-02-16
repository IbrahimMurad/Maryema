import uuid

from django.test import RequestFactory, TestCase

from product.models import Color
from product.serializers import ColorSerializer
from product.serializers.color import NestedColorSerializer
from product.tests.factories import ColorFactory


class ColorSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory().get("/")

    def test_serializer_contains_expected_fields(self):
        color = ColorFactory()
        serializer = ColorSerializer(color, context={"request": self.request})
        self.assertCountEqual(
            serializer.data.keys(),
            [
                "id",
                "created_at",
                "updated_at",
                "color1_name",
                "color1_value",
                "color2_name",
                "color2_value",
                "url",
            ],
        )

    def test_serializer_single_color_validation(self):
        valid_data = {
            "color1_name": "Red",
            "color1_value": "#FF0000",
        }
        serializer = ColorSerializer(data=valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.validated_data, valid_data)
        color = serializer.save()
        self.assertEqual(color.color1_name, "Red")
        self.assertEqual(color.color1_value, "#FF0000")
        self.assertIsNone(color.color2_name)
        self.assertIsNone(color.color2_value)
        self.assertIsNotNone(color.id)
        self.assertIsNotNone(color.created_at)
        self.assertIsNotNone(color.updated_at)

    def test_many_color_serialization(self):
        colors = ColorFactory.create_batch(5)
        serializer = ColorSerializer(
            colors, many=True, context={"request": self.request}
        )
        self.assertEqual(len(serializer.data), 5)
        self.assertEqual(len(serializer.data), Color.objects.count())

    def test_serializer_dual_color_validation(self):
        valid_data = {
            "color1_name": "Red",
            "color1_value": "#FF0000",
            "color2_name": "Blue",
            "color2_value": "#0000FF",
        }
        serializer = ColorSerializer(data=valid_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_color_value(self):
        invalid_data = {
            "color1_name": "Red",
            "color1_value": "FF0000",
        }
        serializer = ColorSerializer(
            data=invalid_data, context={"request": self.request}
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {"color1_value": ["This is not a valid color"]},
        )

    def test_serializer_dual_color(self):
        color = ColorFactory(dual=True)
        serializer = ColorSerializer(color, context={"request": self.request})
        self.assertEqual(
            serializer.data["url"],
            f"http://testserver/api/colors/{color.id}/",
        )
        self.assertEqual(
            serializer.data["color1_name"],
            color.color1_name,
        )
        self.assertEqual(
            serializer.data["color1_value"],
            color.color1_value,
        )
        self.assertEqual(
            serializer.data["color2_name"],
            color.color2_name,
        )
        self.assertEqual(
            serializer.data["color2_value"],
            color.color2_value,
        )
        self.assertEqual(
            serializer.data["url"],
            f"http://testserver/api/colors/{color.id}/",
        )

    def test_non_valid_color_value(self) -> None:
        data = {"color1_name": "Red", "color1_value": "FF0000"}
        serializer = ColorSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {"color1_value": ["This is not a valid color"]},
        )

    def test_update(self) -> None:
        data = {"color1_name": "Red", "color1_value": "#FF0000"}
        color = ColorFactory()
        serializer = ColorSerializer(
            instance=color, data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        color.refresh_from_db()
        self.assertEqual(color.color1_name, "Red")
        self.assertEqual(color.color1_value, "#FF0000")
        self.assertEqual(color.color2_name, None)
        self.assertEqual(color.color2_value, None)

    def test_add_second_color(self) -> None:
        data = {"color2_name": "Red", "color2_value": "#FF0000"}
        color = ColorFactory()
        serializer = ColorSerializer(instance=color, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        color.refresh_from_db()
        self.assertEqual(color.color2_name, "Red")
        self.assertEqual(color.color2_value, "#FF0000")

    def test_missing_required_field(self) -> None:
        data = {"color1_value": "#000000"}
        serializer = ColorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["color1_name"][0].code,
            "required",
        )

    def test_read_only_fields(self) -> None:
        color = ColorFactory()
        color_id = color.id
        data = {"id": uuid.uuid4()}
        serializer = ColorSerializer(instance=color, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        serializer.save()
        color.refresh_from_db()
        self.assertEqual(color.id, color_id)


class NestedColorSerializerTest(TestCase):
    def test_serializer_contains_expected_fields(self):
        color = ColorFactory()
        serializer = NestedColorSerializer(color)
        self.assertCountEqual(
            serializer.data.keys(),
            [
                "id",
                "color1_name",
                "color1_value",
                "color2_name",
                "color2_value",
            ],
        )

    def test_no_deserialization(self):
        data = {
            "color1_name": "Red",
            "color1_value": "#FF0000",
            "color2_name": "Blue",
            "color2_value": "#0000FF",
        }
        serializer = NestedColorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})

    def test_many_color_serialization(self):
        """Test that all he fields are read only"""
        colors = ColorFactory.create_batch(5)
        serializer = NestedColorSerializer(colors, many=True)
        self.assertEqual(len(serializer.data), 5)
        self.assertEqual(len(serializer.data), Color.objects.count())
