# Generated by Django 5.1.2 on 2024-12-24 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("discount", "0001_initial"),
        ("product", "0001_initial"),
        ("profile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="discountrule",
            name="entitled_collection",
            field=models.ManyToManyField(
                help_text="The collections that are eligible for the discount rule. Requires target selection to be selected.",
                related_name="discounts",
                related_query_name="discount",
                to="product.collection",
            ),
        ),
        migrations.AddField(
            model_name="discountrule",
            name="entitled_products",
            field=models.ManyToManyField(
                help_text="The products that are eligible for the discount rule. Requires target selection to be selected.",
                related_name="discounts",
                related_query_name="discount",
                to="product.product",
            ),
        ),
        migrations.AddField(
            model_name="discountrule",
            name="entitled_variants",
            field=models.ManyToManyField(
                help_text="The variants that are eligible for the discount rule. Requires target selection to be selected.",
                related_name="discounts",
                related_query_name="discount",
                to="product.productvariant",
            ),
        ),
        migrations.AddField(
            model_name="discountrule",
            name="prerequisite_collections",
            field=models.ManyToManyField(
                help_text="The collections that will be a prerequisites for a Buy X Get Y type discount.",
                to="product.collection",
            ),
        ),
        migrations.AddField(
            model_name="discountrule",
            name="prerequisite_products",
            field=models.ManyToManyField(
                help_text="The products that will be a prerequisites for a Buy X Get Y type discount.",
                to="product.product",
            ),
        ),
        migrations.AddField(
            model_name="discountrule",
            name="prerequisite_variants",
            field=models.ManyToManyField(
                help_text="The product variants that will be a prerequisites for a Buy X Get Y type discount.",
                to="product.productvariant",
            ),
        ),
        migrations.AddField(
            model_name="discountrule",
            name="selected_customers",
            field=models.ManyToManyField(
                help_text="The customers who are eligible for the discount rule. Requires customer selection to be selected.",
                related_name="discounts",
                related_query_name="discount",
                to="profile.profile",
            ),
        ),
        migrations.AddField(
            model_name="discountcode",
            name="discount_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="discount.discountrule"
            ),
        ),
        migrations.AddField(
            model_name="prerequisitetoentitlementquantityratio",
            name="discount_rule",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prerequisite_to_entitlement_quantity_ratio",
                related_query_name="prerequisite_to_entitlement_quantity_ratio",
                to="discount.discountrule",
            ),
        ),
    ]
