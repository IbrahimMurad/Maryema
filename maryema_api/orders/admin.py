from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ["id", "profile", "total", "status", "discount", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["profile__user__email"]
    date_hierarchy = "created_at"


admin.site.register(Order, OrderAdmin)
