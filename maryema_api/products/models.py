from django.db import models
from django.utils.text import slugify

from core.models import BaseModel
from discounts.models import Discount


class Division(BaseModel):
    """Division model (clothes and accessories)"""

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Division"
        verbose_name_plural = "Divisions"
        db_table = "divisions"

    def __str__(self):
        return slugify(self.name)


class Category(BaseModel):
    """Category model (dresses, pandanas, scarves, etc.)"""

    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name="categories",
        related_query_name="category",
    )
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"

    def __str__(self):
        return self.name


class Product(BaseModel):
    """products model"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="product",
    )
    name = models.CharField(max_length=255)
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

    def __str__(self):
        return self.name
