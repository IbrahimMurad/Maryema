from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ["user", "total", "status"]
    search_fields = ["user__email"]
    readonly_fields = ["total", "total_after_discount"]

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)
