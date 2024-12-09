from django.contrib import admin

from feedbacks.models import Feedback
from products.models import Category, Division, Product


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [FeedbackInline]


admin.site.register(Category)
admin.site.register(Division)
admin.site.register(Product, ProductAdmin)
