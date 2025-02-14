from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase

from product.models import Category, Division
from product.serializers import (
    CategoryNestedSerializer,
    CategorySerializer,
    DivisionNestedCategorySerializer,
)


class CategorySerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.request = RequestFactory().get("/")
        self.division = Division.objects.create(name="Test Division")
        self.category = Category.objects.create(
            name="Test Category", division=self.division
        )

    def test_category_serializer(self) -> None:
        serializer = CategorySerializer(
            instance=self.category, context={"request": self.request}
        )
        data = serializer.data
        self.assertEqual(data["name"], self.category.name)
        self.assertEqual(data["division"], self.division.id)
        self.assertEqual(
            data["url"],
            self.request.build_absolute_uri(f"/api/categories/{self.category.id}/"),
        )

    def test_deserialization(self) -> None:
        data = {"name": "Test Category 2", "division": self.division.id}
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], data["name"])
        self.assertEqual(serializer.validated_data["division"], self.division)

    def test_category_serialization_many(self) -> None:
        clothes = Division.objects.create(name="Clothes")
        shirts = Category.objects.create(name="Shirts", division=clothes)
        pants = Category.objects.create(name="Pants", division=clothes)
        dresses = Category.objects.create(name="Dresses", division=clothes)
        sweaters = Category.objects.create(name="Sweaters", division=clothes)
        hoodies = Category.objects.create(name="Hoodies", division=clothes)

        serializer = CategorySerializer(
            clothes.categories.all(),
            many=True,
            context={"request": self.request},
        )

        data = serializer.data

        self.assertEqual(len(data), 5)
        for category in data:
            self.assertIn(
                category["name"],
                [shirts.name, pants.name, dresses.name, sweaters.name, hoodies.name],
            )
            self.assertEqual(category["division"], clothes.id)

    def test_missing_required_filed(self) -> None:
        data = {"name": "Test Category 2"}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("division", serializer.errors)
        self.assertEqual(serializer.errors["division"][0].code, "required")
        data = {"division": self.division.id}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "required")

    def test_exttra_fields(self) -> None:
        data = {
            "name": "Test Category 2",
            "division": self.division.id,
            "extra": "extra",
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIn("name", serializer.validated_data)
        self.assertIn("division", serializer.validated_data)
        self.assertNotIn("extra", serializer.validated_data)

    def test_unique_name(self) -> None:
        data = {"name": self.category.name, "division": self.division.id}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "unique")

        data = {"name": "   TEST    category    ", "division": self.division.id}
        serializer = CategorySerializer(data=data, context={"request": self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0].code, "unique")

    def test_run_validation_method_for_name(self) -> None:
        data = {"name": "   aNOTHER TEST    category    ", "division": self.division.id}
        serializer = CategorySerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        self.assertIn("name", serializer.validated_data)
        self.assertEqual(serializer.validated_data["name"], "Another Test Category")

    def test_read_only_filed(self) -> None:
        data = {
            "id": self.division.id,
            "name": "Test Category 2",
            "division": self.division.id,
        }
        serializer = CategorySerializer(
            instance=self.category, data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        self.assertIn("name", serializer.validated_data)
        self.assertNotIn("id", serializer.validated_data)

    def test_update(self) -> None:
        data = {"name": "Test Category 2", "division": self.division.id}
        serializer = CategorySerializer(
            instance=self.category, data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, "Test Category 2")


class CategoryNestedSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.request = RequestFactory().get("/")
        self.division = Division.objects.create(name="Test Division")
        self.category = Category.objects.create(
            name="Test Category", division=self.division
        )

    def test_category_nested_serializer(self) -> None:
        serializer = CategoryNestedSerializer(
            instance=self.category, context={"request": self.request}
        )
        data = serializer.data
        self.assertEqual(data["name"], self.category.name)
        self.assertEqual(
            data["url"],
            self.request.build_absolute_uri(f"/api/categories/{self.category.id}/"),
        )
        self.assertNotIn("division", data)
        self.assertIn("id", data)
        self.assertNotIn("created_at", data)
        self.assertNotIn("updated_at", data)

    def test_category_nested_serialization_many(self) -> None:
        clothes = Division.objects.create(name="Clothes")
        shirts = Category.objects.create(name="Shirts", division=clothes)
        pants = Category.objects.create(name="Pants", division=clothes)
        dresses = Category.objects.create(name="Dresses", division=clothes)
        sweaters = Category.objects.create(name="Sweaters", division=clothes)
        hoodies = Category.objects.create(name="Hoodies", division=clothes)

        serializer = CategoryNestedSerializer(
            clothes.categories.all(),
            many=True,
            context={"request": self.request},
        )

        data = serializer.data

        self.assertEqual(len(data), 5)
        for category in data:
            self.assertIn(
                category["name"],
                [shirts.name, pants.name, dresses.name, sweaters.name, hoodies.name],
            )
            self.assertEqual(
                category["url"],
                self.request.build_absolute_uri(f"/api/categories/{category['id']}/"),
            )

    def test_all_are_read_only_fields(self) -> None:
        data = {
            "id": self.category.id,
            "name": "Test Category 2",
            "division": self.division.id,
        }
        serializer = CategoryNestedSerializer(
            instance=self.category, data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("name", serializer.validated_data)
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("url", serializer.validated_data)

    def test_update(self) -> None:
        data = {"name": "Test Category 2", "division": self.division.id}
        serializer = CategoryNestedSerializer(
            instance=self.category, data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        category = serializer.save()
        self.assertEqual(category.name, "Test Category")


class DivisionNestedCategorySerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.request = RequestFactory().get("/")
        self.division = Division.objects.create(name="Test Division")
        self.category = Category.objects.create(
            name="Test Category", division=self.division
        )

    def test_serialization(self) -> None:
        serializer = DivisionNestedCategorySerializer(
            instance=self.category, context={"request": self.request}
        )
        expected_url = self.request.build_absolute_uri(
            f"/api/categories/{self.category.id}/"
        )
        self.assertDictEqual(
            serializer.data,
            {
                "id": str(self.category.id),
                "url": expected_url,
                "name": self.category.name,
                "division": {
                    "id": str(self.division.id),
                    "url": self.request.build_absolute_uri(
                        f"/api/divisions/{self.division.id}/"
                    ),
                    "name": self.division.name,
                },
            },
        )

    def test_serialization_many(self) -> None:
        clothes = Division.objects.create(name="Clothes")
        shirts = Category.objects.create(name="Shirts", division=clothes)
        pants = Category.objects.create(name="Pants", division=clothes)
        dresses = Category.objects.create(name="Dresses", division=clothes)
        sweaters = Category.objects.create(name="Sweaters", division=clothes)
        hoodies = Category.objects.create(name="Hoodies", division=clothes)

        serializer = DivisionNestedCategorySerializer(
            clothes.categories.all(),
            many=True,
            context={"request": self.request},
        )

        data = serializer.data

        self.assertEqual(len(data), 5)
        for category in data:
            self.assertIn(
                category["name"],
                [shirts.name, pants.name, dresses.name, sweaters.name, hoodies.name],
            )
            self.assertEqual(category["division"]["id"], str(clothes.id))
            self.assertEqual(
                category["division"]["url"],
                self.request.build_absolute_uri(f"/api/divisions/{clothes.id}/"),
            )

    def test_no_deserialization(self) -> None:
        """Test that deserialization is not allowed, all the fields are read-only"""
        data = {
            "id": self.category.id,
            "name": "Test Category 2",
            "division": self.division.id,
        }
        # update
        serializer = DivisionNestedCategorySerializer(
            instance=self.category, data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        category = serializer.save()
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.division, self.division)

        # create
        serializer = DivisionNestedCategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        with self.assertRaises(ValidationError):
            category = serializer.save()
