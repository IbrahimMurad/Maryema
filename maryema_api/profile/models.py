""" This module defines the models for profile app
"""

from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel


class Profile(BaseModel):
    """Profile model"""

    class RoleChoices(models.TextChoices):

        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"
        PROVIDER = "provider", "Provider"

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    phone_number = models.CharField(max_length=15, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    role = models.TextField(
        max_length=16, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER
    )
    note = models.TextField(blank=True, default="")
    wishlist = models.ManyToManyField(
        to="product.ProductVariant",
        blank=True,
        related_name="wishlists",
        related_query_name="wishlist",
    )

    class Meta:
        db_table = "profiles"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["user__date_joined"]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username

    @property
    def is_admin(self) -> bool:
        return self.role == self.RoleChoices.ADMIN

    @property
    def is_customer(self) -> bool:
        return self.role == self.RoleChoices.CUSTOMER

    @property
    def is_provider(self) -> bool:
        return self.role == self.RoleChoices.PROVIDER

    @property
    def avatar_url(self) -> str:
        return (
            self.avatar.url
            if self.avatar
            else f"https://avatar.iran.liara.run/public/{51 + (int(self.id) % 50)}"
        )
