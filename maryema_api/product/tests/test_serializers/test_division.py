import uuid

from django.test import RequestFactory, TestCase
from django.utils.timezone import make_naive

from product.models import Division
from product.serializers import DivisionNestedSerializer, DivisionSerializer


class DivisionSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.request = RequestFactory().get("/")

    def test_serialization(self) -> None:
        division = Division.objects.create(name="Clothes")
        serializer = DivisionSerializer(
            instance=division, context={"request": self.request}
        )
        expected_url = self.request.build_absolute_uri(f"/api/divisions/{division.id}/")
        self.assertDictEqual(
            serializer.data,
            {
                "id": str(division.id),
                "url": expected_url,
                "name": "Clothes",
                "created_at": make_naive(division.created_at).astimezone().isoformat(),
                "updated_at": make_naive(division.updated_at).astimezone().isoformat(),
            },
        )

    def test_serialization_many(self) -> None:
        division1 = Division.objects.create(name="Clothes")
        division2 = Division.objects.create(name="Shoes")
        serializer = DivisionSerializer(
            instance=[division1, division2],
            many=True,
            context={"request": self.request},
        )
        expected_url1 = self.request.build_absolute_uri(
            f"/api/divisions/{division1.id}/"
        )
        expected_url2 = self.request.build_absolute_uri(
            f"/api/divisions/{division2.id}/"
        )
        self.assertListEqual(
            serializer.data,
            [
                {
                    "id": str(division1.id),
                    "url": expected_url1,
                    "name": "Clothes",
                    "created_at": make_naive(division1.created_at)
                    .astimezone()
                    .isoformat(),
                    "updated_at": make_naive(division1.updated_at)
                    .astimezone()
                    .isoformat(),
                },
                {
                    "id": str(division2.id),
                    "url": expected_url2,
                    "name": "Shoes",
                    "created_at": make_naive(division2.created_at)
                    .astimezone()
                    .isoformat(),
                    "updated_at": make_naive(division2.updated_at)
                    .astimezone()
                    .isoformat(),
                },
            ],
        )

    def test_deserialization(self) -> None:
        data = {"name": "Division 1"}
        serializer = DivisionSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Division 1")
        division = serializer.save()
        self.assertEqual(division.name, "Division 1")

    def test_missing_required_field(self) -> None:
        data = {}
        serializer = DivisionSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "required")

    def test_unique_field(self) -> None:
        Division.objects.create(name="Division 1")
        data = {"name": "Division 1"}
        serializer = DivisionSerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "unique")

    def test_extra_field(self) -> None:
        data = {"name": "Division 1", "extra": "extra"}
        serializer = DivisionSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        self.assertIn("name", serializer.validated_data)
        self.assertNotIn("extra", serializer.validated_data)

    def test_read_only_field(self) -> None:
        division = Division.objects.create(name="Division 1")
        data = {"id": uuid.uuid4(), "name": "Division 2"}
        serializer = DivisionSerializer(
            instance=division, data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        self.assertIn("name", serializer.validated_data)
        self.assertNotIn("id", serializer.validated_data)

    def test_update(self) -> None:
        division = Division.objects.create(name="Division 1")
        data = {"name": "Division 2"}
        serializer = DivisionSerializer(
            instance=division, data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        division = serializer.save()
        self.assertEqual(division.name, "Division 2")


class DivisionNestedSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.request = RequestFactory().get("/")

    def test_serialization(self) -> None:
        division = Division.objects.create(name="Clothes")
        serializer = DivisionNestedSerializer(
            instance=division, context={"request": self.request}
        )
        expected_url = self.request.build_absolute_uri(f"/api/divisions/{division.id}/")
        self.assertDictEqual(
            serializer.data,
            {
                "id": str(division.id),
                "url": expected_url,
                "name": "Clothes",
            },
        )

    def test_serialization_many(self) -> None:
        division1 = Division.objects.create(name="Clothes")
        division2 = Division.objects.create(name="Shoes")
        serializer = DivisionNestedSerializer(
            instance=[division1, division2],
            many=True,
            context={"request": self.request},
        )
        expected_url1 = self.request.build_absolute_uri(
            f"/api/divisions/{division1.id}/"
        )
        expected_url2 = self.request.build_absolute_uri(
            f"/api/divisions/{division2.id}/"
        )
        self.assertListEqual(
            serializer.data,
            [
                {
                    "id": str(division1.id),
                    "url": expected_url1,
                    "name": "Clothes",
                },
                {
                    "id": str(division2.id),
                    "url": expected_url2,
                    "name": "Shoes",
                },
            ],
        )

    def test_deserialization(self) -> None:
        data = {"name": "Division 1"}
        serializer = DivisionNestedSerializer(
            data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
