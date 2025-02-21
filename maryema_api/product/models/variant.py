from django.core.validators import MinValueValidator
from django.db import models

from core.models import BaseModel
from product.models import Color, Img, Product, Size


class ProductVariant(BaseModel):
    """ProductVariant model for storing product variants"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        related_query_name="variant",
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None,
        related_name="variants",
        related_query_name="variant",
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.SET_DEFAULT,
        null=True,
        default=None,
        related_name="variants",
        related_query_name="variant",
    )
    image = models.ForeignKey(
        Img,
        on_delete=models.PROTECT,
        related_name="variants",
        related_query_name="variant",
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The cost on the seller.",
        validators=[MinValueValidator(0)],
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The price for the customer.",
        validators=[MinValueValidator(0)],
    )
    quantity = models.PositiveSmallIntegerField()
    sort_order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        db_table = "variants"
        ordering = ["sort_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "color", "size"], name="unique_variant"
            ),
            models.UniqueConstraint(
                fields=["sort_order", "product"], name="unique_sort_order"
            ),
        ]

    def clean(self, *args, **kwargs) -> None:
        """Override the clean method to ensure price is greater than cost"""
        if self.price and self.cost and self.price < self.cost:
            raise ValueError("Price cannot be less than cost")
        return super().clean()

    def __str__(self) -> str:
        return f"{str(self.product)} - {str(self.color)} - {str(self.size)}"
