"""This module defines the models of the discount app. It contains :
    DiscountRule model : Which defines the rule of the discount.
    PrerequisiteToEntitlementQuantityRatio model : holds more information for Buy X Get Y type
    DiscountCode model : codes generated for a certain rule.
"""

from datetime import datetime
from profile.models import Profile

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from core.models import BaseModel
from product.models import Collection, Product, ProductVariant


class DiscountRule(BaseModel):
    """a Model in which discount rules are defined"""

    class TypeChoices(models.TextChoices):
        """Choices for the type of discount rule"""

        PERCENTAGE = "PERCENTAGE", "percentage"
        FIXED = "FIXED", "fixed"

    class SelectionChoices(models.TextChoices):
        """Choices for the customer and target selection"""

        ALL = "ALL", "all"
        SELECTED = "SELECTED", "selected"

    class AllocationChoices(models.TextChoices):
        """Choices for the allocation method"""

        ACROSS = "ACROSS", "across"
        EACH = "EACH", "each"

    # Time period of the discount rule
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    # Discount rule details
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    value_type = models.CharField(
        max_length=255,
        choices=TypeChoices.choices,
        default=TypeChoices.FIXED,
        help_text="The value type of discount rule (fixed - percentage).",
    )
    value = models.PositiveIntegerField(
        help_text="The value of the discount rule, either it is a fixed amount or a percentage."
    )

    # Customer and target selection
    customer_selection = models.CharField(
        choices=SelectionChoices.choices,
        max_length=8,
        default=SelectionChoices.ALL,
        help_text="The customers selection for the discount rule (all customers or selected individuals).",
    )
    selected_customers = models.ManyToManyField(
        Profile,
        related_name="discounts",
        related_query_name="discount",
        help_text="The customers who are eligible for the discount rule. Requires customer selection to be selected.",
    )

    # Targeted items for the discount rule
    target_selection = models.CharField(
        choices=SelectionChoices.choices,
        max_length=8,
        default=SelectionChoices.ALL,
        help_text="The target selection for the discount rule (all products or selected products).",
    )
    entitled_collection = models.ManyToManyField(
        Collection,
        related_name="discounts",
        related_query_name="discount",
        help_text="The collections that are eligible for the discount rule. Requires target selection to be selected.",
    )
    entitled_products = models.ManyToManyField(
        Product,
        related_name="discounts",
        related_query_name="discount",
        help_text="The products that are eligible for the discount rule. Requires target selection to be selected.",
    )
    entitled_variants = models.ManyToManyField(
        ProductVariant,
        related_name="discounts",
        related_query_name="discount",
        help_text="The variants that are eligible for the discount rule. Requires target selection to be selected.",
    )

    # Prerequisites for the discount rule
    prerequisite_collections = models.ManyToManyField(
        Collection,
        help_text="The collections that will be a prerequisites for a Buy X Get Y type discount.",
    )
    prerequisite_products = models.ManyToManyField(
        Product,
        help_text="The products that will be a prerequisites for a Buy X Get Y type discount.",
    )
    prerequisite_variants = models.ManyToManyField(
        ProductVariant,
        help_text="The product variants that will be a prerequisites for a Buy X Get Y type discount.",
    )
    prerequisite_quantity_range = models.IntegerField(
        default=0,
        help_text="The quantity of a selected cart item must be greater than or equal to this value.",
    )
    prerequisite_subtotal_range = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        help_text="Specifies the minimum cart subtotal required for a discount to apply.",
    )
    prerequisite_to_entitlement_purchase = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        help_text="Specifies the minimum cart subtotal required for the customer to become eligible for an entitlement",
    )

    # Usage limits and allocation
    once_per_customer = models.BooleanField(
        default=False, help_text="The discount rule can be used only once per customer."
    )
    usage_limit = models.PositiveSmallIntegerField(
        default=1,
        help_text="The maximum number of times the price rule can be used, per discount code.",
        validators=[MinValueValidator(1)],
    )
    allocation_method = models.CharField(
        max_length=255,
        choices=AllocationChoices.choices,
        default=AllocationChoices.EACH,
        help_text="The allocation method of the discount rule (across - each).",
    )
    allocation_limit = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=None,
        help_text=(
            "The number of times the discount can be allocated on the cart - if eligible."
            "Null means unlimited use"
        ),
    )

    class Meta:
        db_table = "discount_rule"
        verbose_name = "Discount Rule"
        verbose_name_plural = "Discount Rules"

    def __str__(self) -> str:
        return self.title

    def clean(self, *args, **kwargs) -> None:
        """override clean method to validate the discount rule before saving it to the database"""

        # Check if the end date is greater than the start date
        if self.ends_at < self.starts_at:
            raise ValidationError("End date should be greater than start date")

        # Check if the value is between 0 and 100 for percentage type discount rules
        if self.value_type == self.TypeChoices.PERCENTAGE and (
            self.value < 0 or self.value > 100
        ):
            raise ValidationError("Percentage value should be between 0 and 100")

        # Check if the targeted customers are provided if the customer selection is selected
        if (
            self.customer_selection == self.SelectionChoices.SELECTED
            and not self.selected_customers
        ):
            raise ValidationError("Selected customers should be provided")

        # Check if the entitled items are provided if the target selection is selected
        if self.target_selection == self.SelectionChoices.SELECTED:
            if not any(
                [
                    self.entitled_collection,
                    self.entitled_products,
                    self.entitled_variants,
                ]
            ):
                raise ValidationError("Entitled items should be provided")

            # ensures that entitled collections can't be used
            # in combination with entitled_products or entitled_variants.
            if self.entitled_collection and any(
                [self.entitled_products, self.entitled_variants]
            ):
                raise ValidationError(
                    (
                        "Entitled collections can't be used in combination with"
                        "entitled products or variants"
                    )
                )

            # ensures that entitled variants do not include any variant
            # that is associated with a product in entitled products
            if variants_included_in_products := self.entitled_variants.filter(
                product__in=self.entitled_products
            ):
                raise ValidationError(
                    (
                        "The following variants are already included in the entitled products:\n"
                        f"\t- {'\n\t- '.join(str(variants_included_in_products))}"
                    )
                )

        # validates the prerequisites for the discount rule if it is a Buy X Get Y type discount
        if any(
            [
                self.prerequisite_collections,
                self.prerequisite_products,
                self.prerequisite_variants,
            ]
        ):
            if self.target_selection != self.SelectionChoices.SELECTED:
                raise ValidationError(
                    "Prerequisites can only be used with selected products, collections, or variants"
                )
            if self.allocation_method != self.AllocationChoices.EACH:
                raise ValidationError(
                    "Prerequisites can only be used with each allocation method"
                )

        return super().clean(*args, **kwargs)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)


class PrerequisiteToEntitlementQuantityRatio(BaseModel):
    """a Model that holds the ratio between the prerequisite quantity and the entitlement quantity"""

    discount_rule = models.OneToOneField(
        DiscountRule,
        on_delete=models.CASCADE,
        related_name="prerequisite_to_entitlement_quantity_ratio",
        related_query_name="prerequisite_to_entitlement_quantity_ratio",
    )
    prerequisite_quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    entitled_quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        db_table = "prerequisite_to_entitlement_quantity_ratio"
        verbose_name = "Prerequisite to Entitlement Quantity Ratio"
        verbose_name_plural = "Prerequisite to Entitlement Quantity Ratios"

    def __str__(self) -> str:
        return f"Buy {self.prerequisite_quantity} get {self.entitled_quantity}"

    def clean(self, *args, **kwargs) -> None:
        """override clean method to validate the ratio before saving it to the database"""

        # ensures that:
        # - value_type set to percentage,
        # - target_type set to line_item,
        # - target_selection set to entitled,
        # - allocation_method set to each,
        # - prerequisite_products or prerequisite_variants or prerequisite_collections defined and
        # - entitled_products or entitled_variants or entitled_collections defined.
        if not all(
            [
                self.discount_rule.value_type == DiscountRule.TypeChoices.PERCENTAGE,
                self.discount_rule.target_selection
                == DiscountRule.SelectionChoices.SELECTED,
                self.discount_rule.allocation_method
                == DiscountRule.AllocationChoices.EACH,
                any(
                    [
                        self.discount_rule.prerequisite_collections,
                        self.discount_rule.prerequisite_products,
                        self.discount_rule.prerequisite_variants,
                    ]
                ),
                any(
                    [
                        self.discount_rule.entitled_collection,
                        self.discount_rule.entitled_products,
                        self.discount_rule.entitled_variants,
                    ]
                ),
            ]
        ):
            raise ValidationError(
                "The ratio can only be used with Buy X Get Y type discount rules"
            )


class DiscountCode(BaseModel):
    """a Model that holds the codes of the discount rules"""

    discount_rule = models.ForeignKey(DiscountRule, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    usage_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "discount_code"
        verbose_name = "Discount Code"
        verbose_name_plural = "Discount Codes"

    def __str__(self) -> str:
        return self.code

    def clean(self, *args, **kwargs) -> None:
        """adding more validations"""

        if self.ends_at < self.starts_at:
            raise ValidationError("End date should be greater than start date")
        if self.usage_count > self.discount_rule.usage_limit:
            raise ValidationError("Usage limit has been reached for this discount code")
        return super().clean(*args, **kwargs)

    def save(self, *args, **kwargs) -> None:
        """berform a full clean before saving it to the database"""

        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def is_active(self) -> bool:
        """returns true if the code is still eligable to use"""
        return (
            self.starts_at <= datetime.now() <= self.ends_at
            and self.usage_count < self.discount_rule.usage_limit
        )
