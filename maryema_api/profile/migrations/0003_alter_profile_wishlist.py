# Generated by Django 5.1.2 on 2025-01-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "product",
            "0009_alter_productvariant_color_alter_productvariant_size_and_more",
        ),
        ("profile", "0002_alter_profile_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="wishlist",
            field=models.ManyToManyField(
                blank=True,
                related_name="wished_by",
                related_query_name="wishlist",
                to="product.productvariant",
            ),
        ),
    ]
