# Generated by Django 5.1.2 on 2024-12-24 09:55

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DiscountCode",
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
                ("code", models.CharField(max_length=255, unique=True)),
                ("starts_at", models.DateTimeField()),
                ("ends_at", models.DateTimeField()),
                ("usage_count", models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Discount Code",
                "verbose_name_plural": "Discount Codes",
                "db_table": "discount_code",
            },
        ),
        migrations.CreateModel(
            name="DiscountRule",
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
                ("starts_at", models.DateTimeField()),
                ("ends_at", models.DateTimeField()),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "value_type",
                    models.CharField(
                        choices=[("PERCENTAGE", "percentage"), ("FIXED", "fixed")],
                        default="FIXED",
                        help_text="The value type of discount rule (fixed - percentage).",
                        max_length=255,
                    ),
                ),
                (
                    "value",
                    models.PositiveIntegerField(
                        help_text="The value of the discount rule, either it is a fixed amount or a percentage."
                    ),
                ),
                (
                    "customer_selection",
                    models.CharField(
                        choices=[("ALL", "all"), ("SELECTED", "selected")],
                        default="ALL",
                        help_text="The customers selection for the discount rule (all customers or selected individuals).",
                        max_length=8,
                    ),
                ),
                (
                    "target_selection",
                    models.CharField(
                        choices=[("ALL", "all"), ("SELECTED", "selected")],
                        default="ALL",
                        help_text="The target selection for the discount rule (all products or selected products).",
                        max_length=8,
                    ),
                ),
                (
                    "prerequisite_quantity_range",
                    models.IntegerField(
                        default=0,
                        help_text="The quantity of a selected cart item must be greater than or equal to this value.",
                    ),
                ),
                (
                    "prerequisite_subtotal_range",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="Specifies the minimum cart subtotal required for a discount to apply.",
                        max_digits=12,
                    ),
                ),
                (
                    "prerequisite_to_entitlement_purchase",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="Specifies the minimum cart subtotal required for the customer to become eligible for an entitlement",
                        max_digits=12,
                    ),
                ),
                (
                    "once_per_customer",
                    models.BooleanField(
                        default=False,
                        help_text="The discount rule can be used only once per customer.",
                    ),
                ),
                (
                    "usage_limit",
                    models.PositiveSmallIntegerField(
                        default=1,
                        help_text="The maximum number of times the price rule can be used, per discount code.",
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "allocation_method",
                    models.CharField(
                        choices=[("ACROSS", "across"), ("EACH", "each")],
                        default="EACH",
                        help_text="The allocation method of the discount rule (across - each).",
                        max_length=255,
                    ),
                ),
                (
                    "allocation_limit",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        default=None,
                        help_text="The number of times the discount can be allocated on the cart - if eligible.Null means unlimited use",
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Discount Rule",
                "verbose_name_plural": "Discount Rules",
                "db_table": "discount_rule",
            },
        ),
        migrations.CreateModel(
            name="PrerequisiteToEntitlementQuantityRatio",
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
                    "prerequisite_quantity",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "entitled_quantity",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
            ],
            options={
                "verbose_name": "Prerequisite to Entitlement Quantity Ratio",
                "verbose_name_plural": "Prerequisite to Entitlement Quantity Ratios",
                "db_table": "prerequisite_to_entitlement_quantity_ratio",
            },
        ),
    ]
