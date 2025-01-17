from uuid import UUID

from django.db.models import Q
from django.forms import UUIDField
from django_filters import rest_framework as filters

from product.models import Product


class CustomUUIDField(UUIDField):
    """
    Over ride the to_python method to return None if the value is empty or wrong uuid

    This way we can filter the UUIDField with the empty value and wrong UUID
    by returning none filtered queryset

    The reason for handling it from here is that django filter checks the value through django forms fields
    """

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, UUID):
            return super().to_python(value)
        return None


class CustomUUIDFilter(filters.UUIDFilter):
    """
    A custom filter class for the UUIDField that uses the CustomUUIDField instead of the default form.UUIDField
    """

    field_class = CustomUUIDField


class ColorNameFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value in ([], (), {}, "", None):
            return qs

        return qs.filter(
            Q(variant__color__color1_name__icontains=value)
            | Q(variant__color__color2_name__icontains=value)
        )


class ColorValueFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value in ([], (), {}, "", None):
            return qs

        return qs.filter(
            Q(variant__color__color1_value__exact=value)
            | Q(variant__color__color2_value__exact=value)
        )


class ProductFilter(filters.FilterSet):
    """
    A filter class for the Product model
    """

    division = CustomUUIDFilter(
        field_name="category__division",
        lookup_expr="exact",
    )
    color_name = ColorNameFilter()
    color_value = ColorValueFilter()

    min_price = filters.NumberFilter(field_name="variant__price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="variant__price", lookup_expr="lte")
    size = filters.CharFilter(field_name="variant__size__name", lookup_expr="exact")

    class Meta:
        model = Product
        fields = {
            "category": ["exact"],
            "collection": ["exact"],
        }
