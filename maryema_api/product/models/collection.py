from django.db import models

from core.models import BaseModel
from product.models import Product


class Collection(BaseModel):
    """Collection model to group products with similar specifications"""

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default="")
    products = models.ManyToManyField(
        Product, related_name="collections", related_query_name="collection"
    )

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        db_table = "collections"

    def __str__(self) -> str:
        return self.name
