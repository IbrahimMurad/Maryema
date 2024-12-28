from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """ensure a full clean before saving"""
        self.full_clean()
        super().save(*args, **kwargs)
