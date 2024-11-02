# Generated by Django 5.1.2 on 2024-11-02 00:56

import django.db.models.deletion
import stock.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("discounts", "0001_initial"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Size",
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
                    "name",
                    models.CharField(
                        max_length=3, validators=[stock.models.validate_size]
                    ),
                ),
            ],
            options={
                "verbose_name": "Size",
                "verbose_name_plural": "Sizes",
                "db_table": "sizes",
            },
        ),
        migrations.CreateModel(
            name="ProductColor",
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
                    "color_1",
                    models.CharField(
                        max_length=7, validators=[stock.models.validate_color]
                    ),
                ),
                (
                    "color_2",
                    models.CharField(
                        blank=True,
                        help_text="a second color for dual-color products",
                        max_length=7,
                        null=True,
                        validators=[stock.models.validate_color],
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_colored",
                        related_query_name="product_colored",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Color",
                "verbose_name_plural": "Product Colors",
                "db_table": "product_colors",
            },
        ),
        migrations.CreateModel(
            name="Stock",
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
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=stock.models.image_path
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("price", models.PositiveIntegerField()),
                ("profited_price", models.IntegerField()),
                (
                    "discount",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stocks",
                        related_query_name="stock",
                        to="discounts.discount",
                    ),
                ),
                (
                    "product_colored",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stocks",
                        related_query_name="stock",
                        to="stock.productcolor",
                    ),
                ),
                (
                    "size",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stock.size"
                    ),
                ),
            ],
            options={
                "verbose_name": "Stock",
                "verbose_name_plural": "Stocks",
                "db_table": "stocks",
            },
        ),
    ]
