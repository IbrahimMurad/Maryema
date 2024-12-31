import uuid
from datetime import datetime
from profile.models import Profile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from core.utils import create_image
from order.models import Order, OrderItem
from product.models import Category, Color, Division, Img, Product, ProductVariant, Size


class OrderTestCase(TestCase):
    """A test suit for Order model"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="user@test.com", password="testpassword"
        )
        self.customer = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.CUSTOMER
        )

    def test_order_creation(self) -> None:
        """Test order creation"""

        order = Order.objects.create(customer=self.customer)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, Order.StatusChoice.PENDING)
        self.assertEqual(order.total, 0.0)
        self.assertEqual(order.close_reason, "")

    def test_order_str(self) -> None:
        """Test order string representation"""
        order = Order.objects.create(customer=self.customer)
        self.assertEqual(
            str(order), f"Order {order.id} - {self.customer.user.username}"
        )

    def test_customer_is_required(self) -> None:
        """Test if customer is required"""
        with self.assertRaises(ValidationError):
            Order.objects.create()

    def test_order_inheritance_from_basemodel(self) -> None:
        """Test order inheritance from BaseModel"""
        order = Order.objects.create(customer=self.customer)
        self.assertTrue(hasattr(order, "id"))
        self.assertIsInstance(order.id, uuid.UUID)
        self.assertTrue(hasattr(order, "created_at"))
        self.assertIsInstance(order.created_at, datetime)
        self.assertTrue(hasattr(order, "updated_at"))
        self.assertIsInstance(order.updated_at, datetime)

    def test_order_status_default_value(self) -> None:
        """Test that order status has deault value of PENDING"""
        order = Order.objects.create(customer=self.customer)
        self.assertEqual(order.status, Order.StatusChoice.PENDING)

    def test_order_status_with_status_out_of_choices(self) -> None:
        """Test that order status must be one of the choices"""
        with self.assertRaises(ValidationError):
            Order.objects.create(customer=self.customer, status="INVALID")

    def test_order_close_reason_default_value(self) -> None:
        """Test that order close reason has default value of empty string"""
        order = Order.objects.create(customer=self.customer)
        self.assertEqual(order.close_reason, "")

    def test_order_close_reason_with_status_not_closed(self) -> None:
        """Test that order status changes to CLOSED if close reason is provided"""
        order = Order.objects.create(customer=self.customer)
        self.assertEqual(order.status, Order.StatusChoice.PENDING)
        order.close_reason = "Test Reason"
        order.save()
        self.assertEqual(order.status, Order.StatusChoice.CLOSED)

    def test_default_ordering(self) -> None:
        """Test that the default ordering is by created_at in descending order"""
        order1 = Order.objects.create(customer=self.customer)
        order2 = Order.objects.create(customer=self.customer)
        order3 = Order.objects.create(customer=self.customer)
        self.assertListEqual(
            list(Order.objects.all()),
            [order3, order2, order1],
        )

    def test_order_total_max_digits(self) -> None:
        """Test that order total has max digits of 8"""
        with self.assertRaises(ValidationError):
            Order.objects.create(customer=self.customer, total=100000000)

    def test_oder_must_have_items_to_change_its_status_to_processing_or_fulfilled(
        self,
    ) -> None:
        """Test that order must have items to change its status to processing or fulfilled"""
        order = Order.objects.create(customer=self.customer)
        with self.assertRaises(ValidationError):
            order.status = Order.StatusChoice.PROSSISSING
            order.save()
        with self.assertRaises(ValidationError):
            order.status = Order.StatusChoice.FULLFILLED
            order.save()


class OrderItemTestCase(TestCase):
    """A test suit for OrderItem model"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="user@test.com", password="testpassword"
        )
        self.customer = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.CUSTOMER
        )
        self.order = Order.objects.create(customer=self.customer)
        self.division = Division.objects.create(name="Test Division")
        self.category = Category.objects.create(
            name="Test Category", division=self.division
        )
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            description="Test Description",
        )
        self.color = Color.objects.create(color1_name="Black")
        self.size1 = Size.objects.create(name="M")
        self.size2 = Size.objects.create(name="L")
        self.size3 = Size.objects.create(name="XL")
        self.image = Img.objects.create(src=create_image())
        self.variant1 = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size1,
            image=self.image,
            cost=5,
            price=10,
            quantity=10,
            sort_order=1,
        )
        self.variant2 = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size2,
            image=self.image,
            cost=7,
            price=14,
            quantity=10,
            sort_order=2,
        )
        self.variant3 = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size3,
            image=self.image,
            cost=10,
            price=20,
            quantity=10,
            sort_order=3,
        )

    def test_order_item_creation(self) -> None:
        """Test order item creation"""

        order_item = self.order.items.create(product_variant=self.variant1, quantity=1)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product_variant, self.variant1)
        self.assertEqual(order_item.quantity, 1)

    def test_order_item_str(self) -> None:
        """Test order item string representation"""
        order_item = self.order.items.create(product_variant=self.variant1, quantity=1)
        self.assertEqual(
            str(order_item),
            f"Order {order_item.order.id} - {order_item.quantity} x {str(order_item.product_variant)}",
        )

    def test_order_is_required(self) -> None:
        """Test if order is required"""
        with self.assertRaises(ValidationError):
            OrderItem.objects.create(product_variant=self.variant1, quantity=1)

    def test_variant_is_required(self) -> None:
        """Test if variant is required"""
        with self.assertRaises(ValidationError):
            self.order.items.create(quantity=1)

    def test_quantity_default_value(self) -> None:
        """Test if quantity is required"""
        order_item = self.order.items.create(product_variant=self.variant1)
        self.assertEqual(order_item.quantity, 1)

    def test_order_item_inheritance_from_basemodel(self) -> None:
        """Test that order item inherit from BaseModel model"""
        order_item = self.order.items.create(product_variant=self.variant1, quantity=1)
        self.assertTrue(hasattr(order_item, "id"))
        self.assertIsInstance(order_item.id, uuid.UUID)
        self.assertTrue(hasattr(order_item, "created_at"))
        self.assertIsInstance(order_item.created_at, datetime)
        self.assertTrue(hasattr(order_item, "updated_at"))
        self.assertIsInstance(order_item.updated_at, datetime)

    def test_product_variant_in_order_is_unique(self) -> None:
        """Test that a product variant in an order is unique"""
        self.order.items.create(product_variant=self.variant1, quantity=1)
        with self.assertRaises(ValidationError):
            self.order.items.create(product_variant=self.variant1, quantity=1)

    def test_order_items_default_ordering(self) -> None:
        """Test that the default ordering for OrderItem model is created_at in DESC order"""
        order_item1 = self.order.items.create(product_variant=self.variant1, quantity=1)
        order_item2 = self.order.items.create(product_variant=self.variant2, quantity=1)
        order_item3 = self.order.items.create(product_variant=self.variant3, quantity=1)
        self.assertListEqual(
            list(self.order.items.all()),
            [order_item3, order_item2, order_item1],
        )


class OrderSignalsTestCase(TestCase):
    """A test suit for Order signals"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="user@test.com", password="testpassword"
        )
        self.customer = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.CUSTOMER
        )
        self.order = Order.objects.create(customer=self.customer)
        self.division = Division.objects.create(name="Test Division")
        self.category = Category.objects.create(
            name="Test Category", division=self.division
        )
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            description="Test Description",
        )
        self.color = Color.objects.create(color1_name="Black")
        self.size1 = Size.objects.create(name="M")
        self.size2 = Size.objects.create(name="L")
        self.size3 = Size.objects.create(name="XL")
        self.image = Img.objects.create(src=create_image())
        self.variant1 = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size1,
            image=self.image,
            cost=5,
            price=10,
            quantity=10,
            sort_order=1,
        )
        self.variant2 = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size2,
            image=self.image,
            cost=7,
            price=14,
            quantity=10,
            sort_order=2,
        )
        self.variant3 = ProductVariant.objects.create(
            product=self.product,
            color=self.color,
            size=self.size3,
            image=self.image,
            cost=10,
            price=20,
            quantity=10,
            sort_order=3,
        )

    def test_order_total_is_updated_when_order_item_is_created(self) -> None:
        """Test that order total is updated when order item is created"""
        self.order.items.create(product_variant=self.variant1, quantity=1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, 10.0)
        self.order.items.create(product_variant=self.variant2, quantity=1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, 24.0)

    def test_order_total_is_updated_when_order_item_is_updated(self) -> None:
        """Test that order total is updated when order item is updated"""
        order_item = self.order.items.create(product_variant=self.variant1, quantity=1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, 10.0)
        order_item.quantity = 2
        order_item.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, 20.0)

    def test_order_total_is_updated_when_order_item_is_deleted(self) -> None:
        """Test that order total is updated when order item is deleted"""
        item1 = self.order.items.create(product_variant=self.variant1, quantity=1)
        item2 = self.order.items.create(product_variant=self.variant2, quantity=1)
        item3 = self.order.items.create(product_variant=self.variant3, quantity=1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, 44.0)
        item1.delete()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, 34.0)
        item2.delete()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, 20.0)
        item3.delete()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, 0.0)


# TO DO - Tests for discount_codes
