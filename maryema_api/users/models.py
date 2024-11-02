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
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, default="avatars/default.jpg"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.email
