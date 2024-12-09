""" models module for discounts app, in which the Discount model is defined.
Discount model represents a discount that can be applied to a product or an order.
product discount: all customers benifit from it and order discount is for a specific customer's order.
"""

from datetime import datetime, timedelta

from django.core.validators import MinValueValidator
from django.db import models

from core.models import BaseModel


def end_date() -> datetime:
    """a callable for the end date of the discount
    which is the same moment in the next day (24 hours later)"""
    return datetime.now() + timedelta(days=1)


class Discount(BaseModel):
    """Discount model"""

    discount_type = models.CharField(
        max_length=255,
        help_text=(
            "a string representing the reason of the discount,"
            "e.g. eid discount, black friday, special offer for Eisha ,etc."
        ),
    )
    code = models.CharField(
        max_length=255,
        unique=True,
        help_text="a unique code for the discount",
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(10)],
        help_text="discount amount as a fixed number",
    )
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(default=end_date)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"
        db_table = "discounts"

    def __str__(self) -> str:
        return self.discount_type + " - " + str(self.amount)
