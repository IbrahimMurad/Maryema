from django.db import models

from core.models import BaseModel


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
