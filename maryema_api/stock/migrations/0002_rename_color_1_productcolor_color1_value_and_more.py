# Generated by Django 5.1.2 on 2024-12-07 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="productcolor",
            old_name="color_1",
            new_name="color1_value",
        ),
        migrations.RenameField(
            model_name="productcolor",
            old_name="color_2",
            new_name="color2_value",
        ),
        migrations.AddField(
            model_name="productcolor",
            name="color1_name",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="productcolor",
            name="color2_name",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
