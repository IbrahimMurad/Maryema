from django.contrib import admin

from stock.models import Color, Size, Stock


class StockInline(admin.TabularInline):
    model = Stock
    extra = 1


class ProductColorAdmin(admin.ModelAdmin):
    inlines = [StockInline]


admin.site.register(Color, ProductColorAdmin)
admin.site.register(Size)
admin.site.register(Stock)
