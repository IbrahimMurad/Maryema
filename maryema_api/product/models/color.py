import re

from django.db import models

from core.models import BaseModel


def validate_color(value: str) -> None:
    """validate that the color is an rgb hexadecimal color code"""
    if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
        raise ValueError("This is not a valid color")


class Color(BaseModel):
    """color model (name and value in hexadecimal) to choose from for the product variants"""

    color1_name = models.CharField(verbose_name="First color name", max_length=20)
    color1_value = models.CharField(
        verbose_name="First color value",
        max_length=7,
        validators=[validate_color],
        null=True,
        blank=True,
    )
    color2_name = models.CharField(
        verbose_name="Second color name", max_length=20, null=True, blank=True
    )
    color2_value = models.CharField(
        verbose_name="Second color value",
        max_length=7,
        validators=[validate_color],
        null=True,
        blank=True,
        help_text="a second color for dual-color products",
    )

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"
        db_table = "colors"

    def __str__(self) -> str:
        return f"{self.color1_name}" + (
            f"-{self.color2_name}" if self.color2_name else ""
        )
