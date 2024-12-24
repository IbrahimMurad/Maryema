""" This module contains the models for the feedback app.
"""

import uuid
from profile.models import Profile

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseModel
from product.models import Product


def is_customer(value: uuid.UUID) -> None:
    """A validator to ensure that the user is a customer"""
    user = Profile.objects.get(pk=value)
    if not user.is_customer:
        raise ValueError("Only customers can give feedbacks.")


class Feedback(BaseModel):
    """Feedback model for customers to rate and comment on products

    Attributes:::

        id: UUID [unique]
        created_at: DateTime [auto_now_add]
        updated_at: DateTime [auto_now]
        customer : Profile object (ForeignKey) [required]
        product : Product object (ForeignKey) [required]
        rate : int [default=0]
        comment : str [optional]
    """

    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        related_query_name="feedback",
        validators=[is_customer],
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        related_query_name="feedback",
        help_text="The product that the feedback is for.",
    )
    rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        help_text="The rate of the product from 1 to 5 (stars). 0 means no rate.",
    )
    comment = models.TextField(
        blank=True, default="", help_text="The comment of the user."
    )

    def __str__(self) -> str:
        return str(self.product) + " - " + str(self.customer)

    class Meta:
        ordering = ["-rate"]
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        db_table = "feedback"
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "product"], name="unique_feedback"
            )
        ]

    def save(self, *args, **kwargs):
        """Override the save method to run a full clean before saving"""
        self.full_clean()
        super().save(*args, **kwargs)
