from django.core.validators import MinValueValidator
from django.db import models

from core.models import BaseModel
from product.models import Color, Img, Product, Size


class ProductVariant(BaseModel):
    """ProductVariant model for storing product variants"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    image = models.ForeignKey(Img, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    sort_order = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        db_table = "variants"
        ordering = ["sort_order"]

    def __str__(self) -> str:
        return f"{str(self.product)} - {str(self.color)} - {str(self.size)}"
