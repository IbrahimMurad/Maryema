from rest_framework import serializers

from discounts.serializers import DiscountSerializer
from stock.models import ProductColor, Size, Stock


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id", "name"]
        read_only_fields = ["id"]


class StockSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = Stock
        fields = ["id", "size", "quantity", "price", "profited_price", "discount"]
        read_only_fields = ["id"]


class ProductColorSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True)

    class Meta:
        model = ProductColor
        fields = [
            "id",
            "color1_name",
            "color1_value",
            "color2_name",
            "color2_value",
            "image",
            "stocks",
        ]
        read_only_fields = ["id"]


class FilterColorSerializer(ProductColorSerializer):
    class Meta(ProductColorSerializer.Meta):
        model = ProductColor
        fields = ["id", "color1_name", "color1_value", "color2_name", "color2_value"]
        read_only_fields = ["id"]
