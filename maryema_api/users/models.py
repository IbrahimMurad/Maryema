""" the models module of the users app
It contains User model that abstract the built-in user model
and make some adjustments to it
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model"""

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.email
