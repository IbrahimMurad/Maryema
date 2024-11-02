from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseModel


def end_date():
    return datetime.now() + timedelta(days=1)


class Discount(BaseModel):
    """Discount model"""

    discount_type = models.CharField(max_length=255)
    discount = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(default=end_date)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"
        db_table = "discounts"

    def __str__(self):
        return self.discount_type + " - " + str(self.discount) + "%"
