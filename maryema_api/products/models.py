""" the models module of the products app
contains the Division, Category, and Product models of the products app.
"""

from django.db import models

from core.models import BaseModel
from discounts.models import Discount


class Division(BaseModel):
    """Division model (clothes and accessories)"""

    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Division"
        verbose_name_plural = "Divisions"
        db_table = "divisions"

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    """Category model (dresses, pandanas, scarves, etc.)"""

    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name="categories",
        related_query_name="category",
    )
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    """products model"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="product",
    )
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        related_query_name="product",
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"

    def __str__(self) -> str:
        return self.name

    @property
    def price(self):
        return self.colors.aggregate(models.Min("stock__price")).get(
            "stock__price__min"
        )

    @property
    def image(self):
        if self.colors.first():
            if self.colors.first().image:
                return self.colors.first().image.url
        return None
