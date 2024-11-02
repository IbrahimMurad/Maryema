# Generated by Django 5.1.2 on 2024-11-02 18:00

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0002_alter_category_name_alter_division_name_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                    "product",
                    models.ForeignKey(
                        help_text="The product that the feedback is for regardless of the color or the size.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        related_query_name="feedback",
                        to="products.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        related_query_name="feedback",
                        to=settings.AUTH_USER_MODEL,
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
