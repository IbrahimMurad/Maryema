from django.db import models

from core.models import BaseModel


class Img(BaseModel):
    """Img model for storing product images"""

    src = models.ImageField(upload_to="product_images")
    alt = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        db_table = "images"

    def __str__(self) -> str:
        return self.alt
