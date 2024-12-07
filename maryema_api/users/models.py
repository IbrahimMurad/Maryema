""" the models module of the users app
It contains User model that abstract the built-in user model
and make some adjustments to it
"""

from django.contrib.auth.models import User
from django.db import models


class AdminManager(models.Manager):
    """a mnager for admins only"""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset(role=Profile.RoleChoices.ADMIN)


class CustomerManager(models.Manager):
    """a mnager for customers only"""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset(role=Profile.RoleChoices.CUSTOMER)


class ProviderManager(models.Manager):
    """a mnager for providers only"""

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset(role=Profile.RoleChoices.PROVIDER)


class Profile(models.Model):
    """User model"""

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
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg")
    role = models.TextField(
        max_length=16, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER
    )

    objects = models.Manager()
    admins = AdminManager()
    customers = CustomerManager()
    providers = ProviderManager()

    class Meta:
        db_table = "users"
        ordering = ["user__date_joined"]

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
