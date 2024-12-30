import uuid
from datetime import datetime
from profile.models import Profile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from feedback.models import Feedback
from product.models import Category, Division, Product


class FeedbackModelTest(TestCase):
    """A test suit for the Feedback model"""

    def setUp(self) -> None:
        """Set up the test environment"""
        self.user = User.objects.create_user(
            username="testuser", email="user@test.com", password="testpassword"
        )
        self.customer = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.CUSTOMER
        )
        self.division = Division.objects.create(name="test division")
        self.category = Category.objects.create(
            division=self.division, name="test category"
        )
        self.product = Product.objects.create(
            category=self.category, name="test product"
        )

    def test_feedback_creation(self) -> None:
        """Test the creation of a feedback"""

        feedback = Feedback.objects.create(
            customer=self.customer,
            product=self.product,
            rate=5,
            comment="Awesome product",
        )
        self.assertEqual(feedback.customer, self.customer)
        self.assertEqual(feedback.product, self.product)
        self.assertEqual(feedback.rate, 5)
        self.assertEqual(feedback.comment, "Awesome product")

    def test_str_representation(self) -> None:
        """Test the string representation of the feedback"""

        feedback = Feedback.objects.create(
            customer=self.customer,
            product=self.product,
            rate=5,
            comment="Awesome product",
        )
        self.assertEqual(str(feedback), f"{self.product} - {self.profile}")

    def test_feedback_inheritance_from_basemodel(self) -> None:
        """Test that the feedback model inherits from the BaseModel"""

        feedback = Feedback.objects.create(
            customer=self.customer,
            product=self.product,
            rate=5,
            comment="Awesome product",
        )
        self.assertTrue(hasattr(feedback, "id"))
        self.assertIsInstance(feedback.id, uuid.UUID)
        self.assertTrue(hasattr(feedback, "created_at"))
        self.assertIsInstance(feedback.created_at, datetime)
        self.assertTrue(hasattr(feedback, "updated_at"))
        self.assertIsInstance(feedback.updated_at, datetime)

    def test_customer_is_required(self) -> None:
        """Test that the customer is required"""

        with self.assertRaises(ValidationError):
            Feedback.objects.create(
                product=self.product, rate=5, comment="Awesome product"
            )

    def test_customer_profile_must_have_role_customer(self) -> None:
        """Test that the customer profile must have role customer"""

        self.customer.role = Profile.RoleChoices.PROVIDER
        self.customer.save()
        with self.assertRaises(ValidationError):
            Feedback.objects.create(
                customer=self.customer,
                product=self.product,
                rate=5,
                comment="Awesome product",
            )

    def test_product_is_required(self) -> None:
        """Test that the product is required"""

        with self.assertRaises(ValidationError):
            Feedback.objects.create(
                customer=self.customer, rate=5, comment="Awesome product"
            )

    def test_rate_default_value(self) -> None:
        """Test that the rate has a default value of 0"""

        feedback = Feedback.objects.create(customer=self.customer, product=self.product)
        self.assertEqual(feedback.rate, 0)

    def test_rate_max_value(self) -> None:
        """Test that the rate has a max value of 5"""

        with self.assertRaises(ValidationError):
            Feedback.objects.create(
                customer=self.customer, product=self.product, rate=6
            )

    def test_comment_is_optional(self) -> None:
        """Test that the comment is optional"""

        feedback = Feedback.objects.create(customer=self.customer, product=self.product)
        self.assertEqual(feedback.comment, "")

    def test_that_default_ordering_is_by_rate_desc(self) -> None:
        """Test that the default ordering is by rate descending"""
        user1 = User.objects.create_user(
            username="testuser1", email="user1@test.com", password="testpassword"
        )
        customer1 = Profile.objects.create(
            user=user1, role=Profile.RoleChoices.CUSTOMER
        )
        user2 = User.objects.create_user(
            username="testuser2", email="user2@test.com", password="testpassword"
        )
        customer2 = Profile.objects.create(
            user=user2, role=Profile.RoleChoices.CUSTOMER
        )
        user3 = User.objects.create_user(
            username="testuser3", email="user3@test.com", password="testpassword"
        )
        customer3 = Profile.objects.create(
            user=user3, role=Profile.RoleChoices.CUSTOMER
        )
        feedback1 = Feedback.objects.create(
            customer=customer1,
            product=self.product,
            rate=5,
            comment="Awesome product",
        )
        feedback2 = Feedback.objects.create(
            customer=customer2,
            product=self.product,
            rate=3,
            comment="Good product",
        )
        feedback3 = Feedback.objects.create(
            customer=customer3,
            product=self.product,
            rate=4,
            comment="Great product",
        )
        feedbacks = Feedback.objects.all()
        self.assertEqual(feedbacks[0], feedback1)
        self.assertEqual(feedbacks[1], feedback3)
        self.assertEqual(feedbacks[2], feedback2)

    def test_feedback_is_unique_for_a_customer_and_a_product(self) -> None:
        """Test that a feedback is unique for a customer and a product"""

        Feedback.objects.create(
            customer=self.customer,
            product=self.product,
            rate=5,
            comment="Awesome product",
        )
        with self.assertRaises(ValidationError):
            Feedback.objects.create(
                customer=self.customer,
                product=self.product,
                rate=4,
                comment="Good product",
            )

    def test_feedback_customer_relation(self) -> None:
        """Test the feedback-customer relation"""

        product1 = Product.objects.create(category=self.category, name="test product 1")
        product2 = Product.objects.create(category=self.category, name="test product 2")
        feedback1 = Feedback.objects.create(
            customer=self.customer,
            product=product1,
            rate=5,
            comment="Awesome product",
        )
        feedback2 = Feedback.objects.create(
            customer=self.customer,
            product=product2,
            rate=5,
            comment="Awesome product",
        )
        self.assertEqual(self.customer.feedbacks.count(), 2)
        self.assertEqual(self.customer.feedbacks.first(), feedback1)
        self.assertEqual(self.customer.feedbacks.last(), feedback2)

    def test_feedback_customer_delete_cascade(self) -> None:
        """Test that the feedbacks are deleted when the customer is deleted"""

        product1 = Product.objects.create(category=self.category, name="test product 1")
        product2 = Product.objects.create(category=self.category, name="test product 2")
        Feedback.objects.create(
            customer=self.customer,
            product=product1,
            rate=5,
            comment="Awesome product",
        )
        Feedback.objects.create(
            customer=self.customer,
            product=product2,
            rate=5,
            comment="Awesome product",
        )
        self.assertEqual(Feedback.objects.count(), 2)
        self.customer.delete()
        self.assertEqual(Feedback.objects.count(), 0)

    def test_feedback_product_relation(self) -> None:
        """Test the feedback-product relation"""

        user1 = User.objects.create_user(
            username="testuser1", email="user1@test.com", password="testpassword"
        )
        customer1 = Profile.objects.create(
            user=user1, role=Profile.RoleChoices.CUSTOMER
        )
        user2 = User.objects.create_user(
            username="testuser2", email="user2@test.com", password="testpassword"
        )
        customer2 = Profile.objects.create(
            user=user2, role=Profile.RoleChoices.CUSTOMER
        )
        user3 = User.objects.create_user(
            username="testuser3", email="user3@test.com", password="testpassword"
        )
        customer3 = Profile.objects.create(
            user=user3, role=Profile.RoleChoices.CUSTOMER
        )
        feedback1 = Feedback.objects.create(
            customer=customer1,
            product=self.product,
            rate=5,
            comment="Awesome product",
        )
        feedback2 = Feedback.objects.create(
            customer=customer2,
            product=self.product,
            rate=3,
            comment="Good product",
        )
        feedback3 = Feedback.objects.create(
            customer=customer3,
            product=self.product,
            rate=4,
            comment="Great product",
        )
        self.assertEqual(self.product.feedbacks.count(), 3)
        self.assertEqual(self.product.feedbacks.first(), feedback1)
        self.assertEqual(self.product.feedbacks.last(), feedback2)
        self.assertIn(feedback3, self.product.feedbacks.all())

    def test_feedback_product_delete_cascade(self) -> None:
        """Test that the feedbacks are deleted when the product is deleted"""

        user1 = User.objects.create_user(
            username="testuser1", email="user1@test.com", password="testpassword"
        )
        customer1 = Profile.objects.create(
            user=user1, role=Profile.RoleChoices.CUSTOMER
        )
        user2 = User.objects.create_user(
            username="testuser2", email="user2@test.com", password="testpassword"
        )
        customer2 = Profile.objects.create(
            user=user2, role=Profile.RoleChoices.CUSTOMER
        )
        user3 = User.objects.create_user(
            username="testuser3", email="user3@test.com", password="testpassword"
        )
        customer3 = Profile.objects.create(
            user=user3, role=Profile.RoleChoices.CUSTOMER
        )
        Feedback.objects.create(
            customer=customer1,
            product=self.product,
            rate=5,
            comment="Awesome product",
        )
        Feedback.objects.create(
            customer=customer2,
            product=self.product,
            rate=3,
            comment="Good product",
        )
        Feedback.objects.create(
            customer=customer3,
            product=self.product,
            rate=4,
            comment="Great product",
        )
        self.assertEqual(Feedback.objects.count(), 3)
        self.product.delete()
        self.assertEqual(Feedback.objects.count(), 0)
