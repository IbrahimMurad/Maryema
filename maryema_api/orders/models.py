"""The models module of the orders app
contains the Order and OrderItem models of the orders app."""

from django.db import models

from core.models import BaseModel
from discounts.models import Discount
from stock.models import Stock
from users.models import Profile


def is_customer(value):
    """Custom validator to check if the user is a customer"""
    if not value.is_customer:
        raise models.ValidationError("The user is not a customer.")
    return value


class Order(BaseModel):
    """Order model"""

    class StatusChoice(models.TextChoices):
        """Status choices for the order model"""

        PENDING = "PENDING", "Pending"
        PROSSISSING = "PROSSISSING", "Prossissing"
        REJECTED = "REJECTED", "Rejected"
        COMPLETED = "COMPLETED", "Completed"
        CANCELED = "CANCELED", "Canceled"

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="orders",
        related_query_name="order",
        validators=[is_customer],
    )
    total = models.DecimalField(decimal_places=2, max_digits=8, default=0.0)
    status = models.CharField(
        max_length=20, choices=StatusChoice.choices, default=StatusChoice.PENDING
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        related_query_name="order",
    )

    def __str__(self) -> str:
        return f"Order {self.id} - {self.profile.user.email}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "orders"

    @property
    def total_after_discount(self) -> float:
        if self.discount:
            return self.total - self.discount.factor * self.total
        return self.total


class OrderItem(BaseModel):
    """Order item model"""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="item",
    )
    product = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="orders",
        related_query_name="order",
    )
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Order {self.order.id} - {str(self.product)} - {self.quantity}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        db_table = "order_items"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"], name="unique_order_item"
            )
        ]
        ordering = ["-created_at"]

    @property
    def total(self) -> float:
        """returns the total price of the product.
        the price of one piece multiplied by the number of ordered pieces."""
        return self.product.price_after_discount * self.quantity
