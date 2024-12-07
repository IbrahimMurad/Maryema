""" the model module of the feedback app
In which Feedback model is defined to store user's feedbacks (rate and comment) for products.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseModel
from products.models import Product
from users.models import Profile as User


def is_customer(value):
    """Custom validator to check if the user is a customer"""
    if not value.is_customer:
        raise models.ValidationError("The user is not a customer.")
    return value


class Feedback(BaseModel):
    """Feedback model for user's feedback"""

    customer = models.ForeignKey(
        User,
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
        help_text="The product that the feedback is for regardless of the color or the size.",
    )
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="The rate of the product from 1 to 5 (stars).",
    )
    comment = models.TextField(
        null=True, blank=True, help_text="The comment of the user."
    )

    def __str__(self):
        return str(self.product) + " - " + str(self.user)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        db_table = "feedback"
