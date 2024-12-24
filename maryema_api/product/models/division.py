from django.db import models

from core.models import BaseModel


class Division(BaseModel):
    """Division model (clothes and accessories)"""

    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Division"
        verbose_name_plural = "Divisions"
        db_table = "divisions"

    def __str__(self) -> str:
        return self.name
