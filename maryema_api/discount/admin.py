from django.contrib import admin

from discount.models import (
    DiscountCode,
    DiscountRule,
    PrerequisiteToEntitlementQuantityRatio,
)

admin.site.register(DiscountRule)
admin.site.register(DiscountCode)
admin.site.register(PrerequisiteToEntitlementQuantityRatio)
