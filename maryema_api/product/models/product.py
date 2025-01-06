from profile.models import Profile

from django.db import models

from core.models import BaseModel
from product.models import Category


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
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"

    def __str__(self) -> str:
        return self.name
