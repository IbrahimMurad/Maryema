""" This module contains the models for the feedback app.
"""

from profile.models import Profile

from django.core.validators import MaxValueValidator
from django.db import models

from core.models import BaseModel
from product.models import Product


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
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        related_query_name="feedback",
        help_text="The product that the feedback is for.",
    )
    rate = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
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
