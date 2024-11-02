from django.contrib import admin

from cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ["user", "total"]
    search_fields = ["user__email"]
    readonly_fields = ["total"]

    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)
