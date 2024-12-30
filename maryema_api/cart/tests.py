import uuid
from datetime import datetime
from io import BytesIO
from profile.models import Profile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from cart.models import Cart, CartItem
from product.models import Category, Color, Division, Img, Product, ProductVariant, Size


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


class CartTestCase(TestCase):
    """A test suit for Cart model"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="user@test.com", password="testpassword"
        )
        self.customer = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.CUSTOMER
        )
        # deactivate the active cart created by the signal
        # in order to make basic test on Cart model
        # since there can only be one active cart for a customer
        cart = self.customer.carts.get(is_active=True)
        cart.is_active = False
        cart.save()
        self.customer.refresh_from_db()

    def test_cart_creation(self) -> None:
        """Test cart creation"""

        cart = Cart.objects.create(customer=self.customer)
        self.assertEqual(cart.customer, self.customer)
        self.assertTrue(cart.is_active)
        self.assertEqual(cart.note, "")
        self.assertEqual(cart.cost, 0)

    def test_cart_str(self) -> None:
        """Test cart string representation"""
        cart = Cart.objects.create(customer=self.customer)
        self.assertEqual(str(cart), f"{str(self.customer)}'s cart")

    def test_customer_is_required(self) -> None:
        """Test if customer is required"""
        with self.assertRaises(ValidationError):
            Cart.objects.create()

    def test_cart_is_active_default_value_is_true(self) -> None:
        """Test if cart is active"""
        cart = Cart.objects.create(customer=self.customer)
        self.assertTrue(cart.is_active)

    def test_cost_default_value(self) -> None:
        """Test cost default value"""
        cart = Cart.objects.create(customer=self.customer)
        self.assertEqual(cart.cost, 0)

    def test_cost_max_digits(self) -> None:
        """Test cost max digits"""
        with self.assertRaises(ValidationError):
            Cart.objects.create(customer=self.customer, cost=99999999999.99)

    def test_cart_inheritance_from_basemodel(self) -> None:
        """Test cart inheritance from BaseModel"""
        cart = Cart.objects.create(customer=self.customer)
        self.assertTrue(hasattr(cart, "id"))
        self.assertIsInstance(cart.id, uuid.UUID)
        self.assertTrue(hasattr(cart, "created_at"))
        self.assertIsInstance(cart.created_at, datetime)
        self.assertTrue(hasattr(cart, "updated_at"))
        self.assertIsInstance(cart.updated_at, datetime)

    def test_unique_customer_active_cart(self) -> None:
        """Test that a customer can only have one active cart"""
        Cart.objects.create(customer=self.customer)
        with self.assertRaises(ValidationError):
            Cart.objects.create(customer=self.customer)

    def test_customer_profile_has_role_customer(self) -> None:
        """Test that the customer profile has role customer"""
        user = User.objects.create_user(
            username="testuser2", email="user123@test.com", password="testpassword"
        )
        profile = Profile.objects.create(user=user, role=Profile.RoleChoices.PROVIDER)
        with self.assertRaises(ValidationError):
            Cart.objects.create(customer=profile)


class CartItemTestCase(TestCase):
    """A test suit for CartItem model"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="user@test.com", password="testpassword"
        )
        self.customer = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.CUSTOMER
        )
        self.cart = Cart.objects.get(customer=self.customer)
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

    def test_cart_item_creation(self) -> None:
        """Test cart item creation"""

        cart_item = self.cart.items.create(product_variant=self.variant1, quantity=1)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product_variant, self.variant1)
        self.assertEqual(cart_item.quantity, 1)

    def test_cart_item_str(self) -> None:
        """Test cart item string representation"""
        cart_item = self.cart.items.create(product_variant=self.variant1, quantity=1)
        self.assertEqual(
            str(cart_item),
            f"{cart_item.product_variant} x {cart_item.quantity} in {cart_item.cart}",
        )

    def test_cart_is_required(self) -> None:
        """Test if cart is required"""
        with self.assertRaises(ValidationError):
            CartItem.objects.create(product_variant=self.variant1, quantity=1)

    def test_variant_is_required(self) -> None:
        """Test if variant is required"""
        with self.assertRaises(ValidationError):
            self.cart.items.create(quantity=1)

    def test_quantity_default_value(self) -> None:
        """Test if quantity is required"""
        cart_item = self.cart.items.create(product_variant=self.variant1)
        self.assertEqual(cart_item.quantity, 1)

    def test_cart_in_cart_item_must_be_active(self) -> None:
        """Test that the cart of the cart item is active"""

        self.cart.is_active = False
        self.cart.save()
        with self.assertRaises(ValidationError):
            CartItem.objects.create(
                cart=self.cart, product_variant=self.variant1, quantity=1
            )

    def test_cart_deleted_variant(self) -> None:
        """Test that the cart item is deleted when the variant is deleted"""

        cart_item = self.cart.items.create(product_variant=self.variant1, quantity=1)
        self.variant1.delete()
        with self.assertRaises(CartItem.DoesNotExist):
            cart_item.refresh_from_db()

    def test_cart_item_deleted_cart(self):
        """Test that the cart item is deleted when the cart is deleted"""

        cart_item = self.cart.items.create(product_variant=self.variant1, quantity=1)
        self.cart.delete()
        with self.assertRaises(CartItem.DoesNotExist):
            cart_item.refresh_from_db()

    def test_cart_item_inheritance_from_basemodel(self) -> None:
        """Test that cart item inherit from BaseModel model"""
        cart_item = self.cart.items.create(product_variant=self.variant1, quantity=1)
        self.assertTrue(hasattr(cart_item, "id"))
        self.assertIsInstance(cart_item.id, uuid.UUID)
        self.assertTrue(hasattr(cart_item, "created_at"))
        self.assertIsInstance(cart_item.created_at, datetime)
        self.assertTrue(hasattr(cart_item, "updated_at"))
        self.assertIsInstance(cart_item.updated_at, datetime)

    def test_product_variant_in_cart_is_unique(self) -> None:
        """Test that a cart item in a cart is unique"""
        self.cart.items.create(product_variant=self.variant1, quantity=1)
        with self.assertRaises(ValidationError):
            self.cart.items.create(product_variant=self.variant1, quantity=1)


class CartAndItemsTestCase(TestCase):
    """A test suit for Cart and CartItem models"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="user@test.com", password="testpassword"
        )
        self.customer = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.CUSTOMER
        )
        self.cart = Cart.objects.get(customer=self.customer)
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

    def test_create_cart_items_from_the_cart(self) -> None:
        """Test create cart items from the cart"""

        item1 = self.cart.items.create(product_variant=self.variant1, quantity=1)
        item2 = self.cart.items.create(product_variant=self.variant2, quantity=2)
        item3 = self.cart.items.create(product_variant=self.variant3, quantity=3)

        self.assertEqual(self.cart.items.count(), 3)
        self.assertIn(item1, self.cart.items.all())
        self.assertIn(item2, self.cart.items.all())
        self.assertIn(item3, self.cart.items.all())

    def test_update_cart_item_from_the_cart(self) -> None:
        """Test update a crt item from the cart"""

        item1 = self.cart.items.create(product_variant=self.variant1, quantity=1)
        self.cart.items.create(product_variant=self.variant2, quantity=2)
        self.cart.items.create(product_variant=self.variant3, quantity=3)

        self.cart.items.filter(product_variant=self.variant1).update(quantity=2)
        item1.refresh_from_db()
        self.assertEqual(item1.quantity, 2)

    def test_remove_item_from_the_cart(self) -> None:
        """Test removing an item from the cart"""

        self.cart.items.create(product_variant=self.variant1, quantity=1)
        self.cart.items.create(product_variant=self.variant2, quantity=2)
        self.cart.items.create(product_variant=self.variant3, quantity=3)

        self.cart.items.filter(product_variant=self.variant1).delete()
        self.assertEqual(self.cart.items.count(), 2)

    def test_clear_cart(self) -> None:
        """Test clearing the cart"""

        self.cart.items.create(product_variant=self.variant1, quantity=1)
        self.cart.items.create(product_variant=self.variant2, quantity=2)
        self.cart.items.create(product_variant=self.variant3, quantity=3)

        self.cart.items.all().delete()
        self.assertEqual(self.cart.items.count(), 0)


# To do test case for discount codes in the the cart
# To do test case for the cart total cost


class CartSignalsTestCase(TestCase):
    """A test suit for Cart signals"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", email="user@test.com", password="testpassword"
        )
        self.customer = Profile.objects.create(
            user=self.user, role=Profile.RoleChoices.CUSTOMER
        )
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

    def test_new_cart_with_new_customer_creation(self) -> None:
        """Test create_cart signal that creates a new active cart once a new customer is created"""

        cart = Cart.objects.filter(customer=self.customer).first()
        self.assertIsNotNone(cart)
        self.assertTrue(cart.is_active)
        self.assertIn(cart, self.customer.carts.all())

    def test_update_cart_cost_when_cart_item_is_created(self) -> None:
        """Test update_cart_cost signal that updates the cost of the cart when a cart item is created"""

        cart = Cart.objects.get(customer=self.customer)
        cart.items.create(product_variant=self.variant1, quantity=1)
        cart.refresh_from_db()
        self.assertEqual(cart.cost, 10)
        cart.items.create(product_variant=self.variant2, quantity=2)
        cart.refresh_from_db()
        self.assertEqual(cart.cost, 38)

    def test_update_cart_cost_when_cart_item_is_updated(self) -> None:
        """Test update_cart_cost signal that updates the cost of the cart when a cart item is updated"""

        cart = Cart.objects.get(customer=self.customer)
        cart_item = cart.items.create(product_variant=self.variant1, quantity=1)
        self.assertEqual(cart.cost, 10)
        cart_item.quantity = 2
        cart_item.save()
        cart.refresh_from_db()
        self.assertEqual(cart.cost, 20)

    def test_update_cart_cost_when_cart_item_is_deleted(self) -> None:
        """Test update_cart_cost signal that updates the cost of the cart when a cart item is deleted"""

        cart = Cart.objects.get(customer=self.customer)
        item1 = cart.items.create(product_variant=self.variant1, quantity=1)
        cart.items.create(product_variant=self.variant2, quantity=2)
        self.assertEqual(cart.cost, 38)
        item1.delete()
        cart.refresh_from_db()
        self.assertEqual(cart.cost, 28)

    def test_update_cart_cost_when_cart_is_cleared(self) -> None:
        """Test update_cart_cost signal that updates the cost of the cart when a cart item is deleted"""

        cart = Cart.objects.get(customer=self.customer)
        cart.items.create(product_variant=self.variant1, quantity=1)
        cart.items.create(product_variant=self.variant2, quantity=2)
        self.assertEqual(cart.cost, 38)
        cart.items.all().delete()
        cart.refresh_from_db()
        self.assertEqual(cart.cost, 0)
