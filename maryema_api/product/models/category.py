from django.db import models

from core.models import BaseModel
from product.models import Division


class Category(BaseModel):
    """Category model (dresses, pandanas, scarves, etc.)"""

    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name="categories",
        related_query_name="category",
    )
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"

    def __str__(self) -> str:
        return self.name
