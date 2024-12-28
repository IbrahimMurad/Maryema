# Generated by Django 5.1.2 on 2024-12-24 09:55

import django.core.validators
import django.db.models.deletion
import product.models.color
import product.models.size
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Collection",
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
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField(blank=True, default="")),
            ],
            options={
                "verbose_name": "Collection",
                "verbose_name_plural": "Collections",
                "db_table": "collections",
            },
        ),
        migrations.CreateModel(
            name="Color",
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
                    "color1_name",
                    models.CharField(max_length=20, verbose_name="First color name"),
                ),
                (
                    "color1_value",
                    models.CharField(
                        max_length=7,
                        validators=[product.models.color.validate_color],
                        verbose_name="First color value",
                    ),
                ),
                (
                    "color2_name",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Second color name",
                    ),
                ),
                (
                    "color2_value",
                    models.CharField(
                        blank=True,
                        help_text="a second color for dual-color products",
                        max_length=7,
                        null=True,
                        validators=[product.models.color.validate_color],
                        verbose_name="Second color value",
                    ),
                ),
            ],
            options={
                "verbose_name": "Color",
                "verbose_name_plural": "Colors",
                "db_table": "colors",
            },
        ),
        migrations.CreateModel(
            name="Division",
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
                ("name", models.CharField(max_length=64)),
            ],
            options={
                "verbose_name": "Division",
                "verbose_name_plural": "Divisions",
                "db_table": "divisions",
            },
        ),
        migrations.CreateModel(
            name="Img",
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
                ("src", models.ImageField(upload_to="product_images")),
                ("alt", models.CharField(max_length=255)),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
                "db_table": "images",
            },
        ),
        migrations.CreateModel(
            name="ProductVariant",
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
                ("cost", models.DecimalField(decimal_places=2, max_digits=10)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "quantity",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("sort_order", models.IntegerField(default=1)),
            ],
            options={
                "verbose_name": "Product Variant",
                "verbose_name_plural": "Product Variants",
                "db_table": "variants",
                "ordering": ["sort_order"],
            },
        ),
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
                        max_length=3, validators=[product.models.size.validate_size]
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
            name="Category",
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
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "division",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="categories",
                        related_query_name="category",
                        to="product.division",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "db_table": "categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "tags",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="comma separated tags for search purpuses",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        related_query_name="product",
                        to="product.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "db_table": "products",
            },
        ),
    ]