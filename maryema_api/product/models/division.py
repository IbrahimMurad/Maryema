from django.db import models

from core.models import BaseModel


class Division(BaseModel):
    """Division model (clothes and accessories)"""

    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Division"
        verbose_name_plural = "Divisions"
        db_table = "divisions"
        ordering = ["name"]

    def clean(self):
        """Capitalize and strip the name before saving to ensure uniqueness"""
        self.name = self.name.strip().capitalize()
        return super().clean()

    def __str__(self) -> str:
        return self.name
