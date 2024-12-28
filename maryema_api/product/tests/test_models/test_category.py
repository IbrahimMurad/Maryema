import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from product.models import Category, Division


class TestCategoryModel(TestCase):
    """A test case for Category model"""

    def setUp(self):
        """setting up a category instance for testing"""
        self.division = Division.objects.create(name="Division 1")

    def test_str(self):
        """Test string representation"""
        division = Category.objects.create(division=self.division, name="Category 1")
        self.assertEqual(str(division), "Category 1")

    def test_required_name(self):
        """test required name field (not null and not blank)"""
        category = Category(division=self.division)
        with self.assertRaises(ValidationError):
            category.save()
        category = Category(division=self.division, name="")
        with self.assertRaises(ValidationError):
            category.save()

    def test_required_division(self):
        """test required division field"""
        category = Category(name="Category 1")
        with self.assertRaises(ValidationError):
            category.save()

    def test_category_inheritance_from_BaseModel(self):
        """Ensure Category model inherit from BaseModel"""
        category = Category.objects.create(division=self.division, name="category 1")
        self.assertIsNotNone(category.id)
        self.assertTrue(isinstance(category.id, uuid.UUID))
        self.assertIsNotNone(category.created_at)
        self.assertTrue(isinstance(category.created_at, datetime))
        self.assertIsNotNone(category.updated_at)
        self.assertTrue(isinstance(category.updated_at, datetime))

    def test_category_division_relation(self):
        """Test the category-division relationship"""
        category = Category.objects.create(division=self.division, name="category 1")
        self.assertEqual(category.division, self.division)
        self.assertEqual(self.division.categories.count(), 1)
        self.assertEqual(self.division.categories.first(), category)

    def test_category_division_deletion(self):
        """Test that a division deletion deletes its categories"""
        Category.objects.create(division=self.division, name="category 1")
        self.division.delete()
        self.assertEqual(Category.objects.count(), 0)
