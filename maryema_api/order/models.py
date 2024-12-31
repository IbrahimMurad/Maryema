""" This module contains the models for the order app
"""

from profile.models import Profile

from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from discount.models import DiscountCode
from product.models import ProductVariant


class Order(BaseModel):
    """Order model

    Attributes:::
        id: UUID [unique]
        created_at: DateTime [auto_now_add]
        updated_at: DateTime [auto_now]
        customer (ForeignKey): The customer who made the order
        status (CharField): The status of the order
        total (DecimalField): The total amount of the order
        close_reason (TextField): The reason for closing the order
    """

    class StatusChoice(models.TextChoices):
        """Status choices for the order model"""

        PENDING = "PENDING", "Pending"
        PROSSISSING = "PROSSISSING", "Prossissing"
        CLOSED = "CLOSED", "Closed"
        FULLFILLED = "FULLFILLED", "Fullfilled"
        CANCELED = "CANCELED", "Canceled"

    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="orders",
        related_query_name="order",
    )
    status = models.CharField(
        max_length=20, choices=StatusChoice.choices, default=StatusChoice.PENDING
    )
    total = models.DecimalField(decimal_places=2, max_digits=8, default=0.0)
    close_reason = models.TextField(blank=True, default="")
    discount_codes = models.ManyToManyField(
        DiscountCode,
        related_name="orders",
        related_query_name="order",
        help_text="List of discount codes that are applied to this order",
    )

    def __str__(self) -> str:
        return f"Order {self.id} - {self.customer.user.username}"

    def clean(self, *args, **kwargs):
        """Override the save method check if the order is closed when close reason is not blank"""
        if self.close_reason and self.status != self.StatusChoice.CLOSED:
            self.status = self.StatusChoice.CLOSED
        if (
            self.status == self.StatusChoice.PROSSISSING
            or self.status == self.StatusChoice.FULLFILLED
        ) and not self.items.exists():
            raise ValidationError(
                "Order must have at least one item to be processed or fullfilled"
            )
        super().clean(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "orders"


class OrderItem(BaseModel):
    """Order item model"""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="item",
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="orders",
        related_query_name="order",
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"Order {self.order.id} - {self.quantity} x {str(self.product_variant)}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        db_table = "order_items"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product_variant"], name="unique_order_item"
            )
        ]
        ordering = ["-created_at"]
