import uuid
from profile.models import Profile

from django.core.exceptions import ValidationError
from django.db import models

from core.models import BaseModel
from product.models import Category


def is_provider(value: uuid.UUID) -> None:
    """Ensures that the profile is a provider"""
    if (
        value is not None
        and not Profile.objects.get(id=value).role == Profile.RoleChoices.PROVIDER
    ):
        raise ValidationError("Profile is not a provider")


class Product(BaseModel):
    """products model"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="product",
    )
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default="")
    tags = models.TextField(
        blank=True, default="", help_text="comma separated tags for search purpuses"
    )
    provider = models.ForeignKey(
        Profile,
        verbose_name="product provider",
        on_delete=models.SET_NULL,
        related_name="products",
        related_query_name="product",
        null=True,
        blank=True,
        validators=[is_provider],
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"

    def __str__(self) -> str:
        return self.name
