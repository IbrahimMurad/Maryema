# Generated by Django 5.1.2 on 2025-01-07 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("discount", "0002_initial"),
        ("order", "0004_rename_customer_order_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="discount_codes",
            field=models.ManyToManyField(
                blank=True,
                help_text="List of discount codes that are applied to this order",
                related_name="orders",
                related_query_name="order",
                to="discount.discountcode",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("processing", "Processing"),
                    ("closed", "Closed"),
                    ("cenceled", "Canceled"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
