""" the models module for the stock app
contains Size, ProductColor, Stock models
"""

import re

from django.db import models
from django.utils.text import slugify

from core.models import BaseModel
from discounts.models import Discount
from products.models import Product


def validate_size(value) -> None:
    """validates the size of the product to be a number
    or a string in [XS, S, M, L, XL, XXL]"""
    if not (value.isdigit() or value in ["XS", "S", "M", "L", "XL", "XXL"]):
        raise ValueError("This is not a valid size")


class Size(BaseModel):
    """Size model - specifies the size of the product"""

    name = models.CharField(max_length=3, validators=[validate_size])

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        db_table = "sizes"

    def __str__(self) -> str:
        return self.name


def validate_color(value) -> None:
    """validate that the color is an rgb hexadecimal color code"""
    if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
        raise ValueError("This is not a valid color")


def image_path(instance, file_name) -> str:
    return (
        f"products/{slugify(instance.product.name)}/{instance.color1_name}/{file_name}"
    )


class ProductColor(BaseModel):
    """procut_color model (hexadecimal) - the product and its rgb color code"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="colors",
        related_query_name="color",
    )

    color1_name = models.CharField(max_length=20)
    color1_value = models.CharField(max_length=7, validators=[validate_color])
    color2_name = models.CharField(max_length=20, null=True, blank=True)
    color2_value = models.CharField(
        max_length=7,
        validators=[validate_color],
        null=True,
        blank=True,
        help_text="a second color for dual-color products",
    )
    image = models.ImageField(upload_to=image_path, null=True, blank=True)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"
        db_table = "product_colors"

    def __str__(self) -> str:
        return f"{str(self.product)} - {self.color1_name}" + (
            f"-{self.color2_name}" if self.color2_name else ""
        )


class Stock(BaseModel):
    """Stock model"""

    product_colored = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        related_name="stocks",
        related_query_name="stock",
    )

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
        ordering = ["price"]

    def __str__(self) -> str:
        return f"{self.product_colored} - {self.size}"

    @property
    def product(self) -> Product:
        """returns the product of the stock"""
        return self.product_colored.product

    @property
    def selling_price(self) -> int:
        """returns the price of the stock after adding profit"""
        return self.price + self.profited_price

    @property
    def price_after_discount(self) -> int:
        """returns the price after applying the discount"""
        if self.discount:
            return self.selling_price - self.discount.amount
        return self.selling_price
