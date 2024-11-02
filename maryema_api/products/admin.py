from django.contrib import admin

from products.models import Category, Division, Product

admin.site.register(Category)
admin.site.register(Division)
admin.site.register(Product)
