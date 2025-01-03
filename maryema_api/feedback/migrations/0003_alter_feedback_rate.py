# Generated by Django 5.1.2 on 2024-12-30 08:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="rate",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text="The rate of the product from 1 to 5 (stars). 0 means no rate.",
                validators=[django.core.validators.MaxValueValidator(5)],
            ),
        ),
    ]
