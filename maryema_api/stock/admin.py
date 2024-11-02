from django.contrib import admin

from stock.models import ProductColor, Size, Stock

admin.site.register(ProductColor)
admin.site.register(Size)
admin.site.register(Stock)
