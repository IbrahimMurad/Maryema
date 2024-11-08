# Generated by Django 5.1.2 on 2024-11-01 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="avatars/default.jpg",
                null=True,
                upload_to="avatars/",
            ),
        ),
    ]
