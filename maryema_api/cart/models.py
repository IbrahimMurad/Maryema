""" This module contains the models for the cart app
"""

import uuid
from profile.models import Profile

from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel

# from discount.models import DiscountCode
from product.models import ProductVariant


def is_customer(value: uuid.UUID) -> None:
    """Ensures that the cart is associated with a customer"""
    if not Profile.objects.get(id=value).is_customer:
        raise ValidationError("The cart must be associated with a customer")


class Cart(BaseModel):
    """Cart model that represents a cart

    Attributes:::

        id: UUID [unique]
        created_at: DateTime [auto_now_add]
        updated_at: DateTime [auto_now]
        customer : Profile object (ForeignKey) [required]
        is_active : bool [default=True]
        note : str [optional]
        cost : Decimal [default=0]
    """

    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        validators=[is_customer],
        related_name="carts",
        related_query_name="cart",
    )
    is_active = models.BooleanField(
        default=True, help_text="True if cart is active, False if cart is inactive"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="The estimated cost that the buyer will pay at checkout, including subtotals, discounts, and total amounts.",
    )

    def __str__(self) -> str:
        return f"{str(self.customer)}'s cart"

    class Meta:
        verbose_name_plural = "Carts"
        db_table = "cart"
        constraints = [
            models.UniqueConstraint(
                fields=["customer"],
                condition=models.Q(is_active=True),
                name="unique_active_cart",
            )
        ]


def is_active_cart(value: uuid.UUID) -> None:
    """Ensures that the cart is active"""
    if not Cart.objects.get(id=value).is_active:
        raise ValidationError("The cart must be active")


class CartItem(BaseModel):
    """CartItem model that represents an item in a cart

    Attributes:::

        id: UUID [unique]
        created_at: DateTime [auto_now_add]
        updated_at: DateTime [auto_now]
        cart : Cart object (ForeignKey) [required]
        product_variant : ProductVariant object (ForeignKey) [required]
        quantity : int [default=1] [required]
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="item",
        validators=[is_active_cart],
    )
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    # discount_codes = models.ManyToManyField(DiscountCode)

    class Meta:
        db_table = "cart_item"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product_variant"],
                name="unique_cart_item",
            )
        ]

    def __str__(self) -> str:
        return f"{self.product_variant} x {self.quantity} in {self.cart}"
