from django.contrib import admin

from product.models import (
    Category,
    Collection,
    Color,
    Division,
    Img,
    Product,
    ProductVariant,
    Size,
)

admin.site.register(Category)
admin.site.register(Division)
admin.site.register(Product)
admin.site.register(Collection)
admin.site.register(ProductVariant)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Img)
