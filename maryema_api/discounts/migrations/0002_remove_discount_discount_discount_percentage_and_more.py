# Generated by Django 5.1.2 on 2024-11-02 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("discounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="discount",
            name="discount",
        ),
        migrations.AddField(
            model_name="discount",
            name="percentage",
            field=models.FloatField(
                default=0.0,
                help_text="discount percentage as a float number between 0 and 100",
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(100.0),
                ],
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="discount",
            name="discount_type",
            field=models.CharField(
                help_text="a string representing the reason of the discount,e.g. eid discount, black friday, special offer for Eisha ,etc.",
                max_length=255,
            ),
        ),
    ]
