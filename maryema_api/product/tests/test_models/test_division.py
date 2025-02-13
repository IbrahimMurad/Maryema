import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from product.models import Division


class TestDivisionModel(TestCase):
    """A test case for Division model"""

    def test_str(self) -> None:
        """Test string representation"""
        division = Division.objects.create(name="Division 1")
        self.assertEqual(str(division), "Division 1")

    def test_required_name(self) -> None:
        """test required name field (not null and not blank)"""
        division = Division()
        with self.assertRaises(ValidationError):
            division.save()
        division = Division(name="")
        with self.assertRaises(ValidationError):
            division.save()

    def test_division_inheritance_from_BaseModel(self) -> None:
        """Ensure Division model inherit from BaseModel"""
        division = Division.objects.create(name="Division 1")
        self.assertIsNotNone(division.id)
        self.assertTrue(isinstance(division.id, uuid.UUID))
        self.assertIsNotNone(division.created_at)
        self.assertTrue(isinstance(division.created_at, datetime))
        self.assertIsNotNone(division.updated_at)
        self.assertTrue(isinstance(division.updated_at, datetime))

    def test_unique_division_name(self) -> None:
        """Test unique name field"""
        Division.objects.create(name="Division 1")
        with self.assertRaises(ValidationError):
            Division.objects.create(name="Division 1")

    def test_clean_name(self) -> None:
        """Test clean method"""
        division = Division.objects.create(name="division 1")
        self.assertEqual(division.name, "Division 1")
        division = Division.objects.create(name="  division 2  ")
        self.assertEqual(division.name, "Division 2")
        division = Division.objects.create(name="  DIVISION 3  ")
        self.assertEqual(division.name, "Division 3")
        self.assertRaises(ValidationError, Division.objects.create, name="division 3")
