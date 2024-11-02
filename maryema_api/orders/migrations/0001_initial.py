# Generated by Django 5.1.2 on 2024-11-02 18:00

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("discounts", "0002_remove_discount_discount_discount_percentage_and_more"),
        ("stock", "0002_remove_stock_image_productcolor_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                    "total",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("PROSSISSING", "Prossissing"),
                            ("REJECTED", "Rejected"),
                            ("COMPLETED", "Completed"),
                            ("CANCELED", "Canceled"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                (
                    "discount",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orders",
                        related_query_name="order",
                        to="discounts.discount",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        related_query_name="order",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
                "db_table": "orders",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("quantity", models.PositiveIntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        related_query_name="item",
                        to="orders.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        related_query_name="order",
                        to="stock.stock",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order Item",
                "verbose_name_plural": "Order Items",
                "db_table": "order_items",
                "ordering": ["-created_at"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("order", "product"), name="unique_order_item"
                    )
                ],
            },
        ),
    ]
