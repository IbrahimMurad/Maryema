import re

from django.db import models
from django.utils.text import slugify

from core.models import BaseModel
from discounts.models import Discount
from products.models import Product


def validate_size(value):
    if not value.isdigit() or value not in ["XS", "S", "M", "L", "XL", "XXL"]:
        raise ValueError("This is not a valid size")


class Size(BaseModel):
    """Size model"""

    name = models.CharField(max_length=3, validators=[validate_size])

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        db_table = "sizes"

    def __str__(self):
        return self.name


def validate_color(value):
    if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
        raise ValueError("This is not a valid color")


class ProductColor(BaseModel):
    """procut_color model (hexadecimal) - the rgb color code of the product"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_colored",
        related_query_name="product_colored",
    )

    color_1 = models.CharField(max_length=7, validators=[validate_color])
    color_2 = models.CharField(
        max_length=7,
        validators=[validate_color],
        null=True,
        blank=True,
        help_text="a second color for dual-color products",
    )

    class Meta:
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"
        db_table = "product_colors"

    def __str__(self):
        return f"{str(self.product)} - {self.color_1[1:]}" + (
            f"-{self.color_2[1:]}" if self.color_2 else ""
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        # fill color_2 with color_1 if color_2 is empty
        if not self.color_2:
            self.color_2 = self.color_1
        super().save(*args, **kwargs)


def image_path(instance, _):
    return f"products/{slugify(instance.product_colored.product.name)}-{str(instance.product_colored)}"


class Stock(BaseModel):
    """Stock model"""

    product_colored = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        related_name="stocks",
        related_query_name="stock",
    )

    image = models.ImageField(upload_to=image_path, null=True, blank=True)

    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    price = models.PositiveIntegerField()
    profited_price = models.IntegerField()

    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stocks",
        related_query_name="stock",
    )

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        db_table = "stocks"

    def __str__(self):
        return f"{self.product} - {self.size} - {self.color}"
