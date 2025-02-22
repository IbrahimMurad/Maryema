# Generated by Django 5.1.2 on 2025-02-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0011_alter_category_options_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="category",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
