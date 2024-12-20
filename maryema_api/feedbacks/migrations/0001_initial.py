# Generated by Django 5.1.2 on 2024-12-06 02:36

import django.core.validators
import django.db.models.deletion
import feedbacks.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "rate",
                    models.IntegerField(
                        blank=True,
                        help_text="The rate of the product from 1 to 5 (stars).",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True, help_text="The comment of the user.", null=True
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        related_query_name="feedback",
                        to="users.customuser",
                        validators=[feedbacks.models.is_customer],
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="The product that the feedback is for regardless of the color or the size.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        related_query_name="feedback",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Feedback",
                "verbose_name_plural": "Feedbacks",
                "db_table": "feedback",
                "ordering": ["-created_at"],
            },
        ),
    ]
