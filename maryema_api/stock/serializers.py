from rest_framework import serializers

from discounts.serializers import DiscountSerializer
from stock.models import Color, Size, Stock


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"
        read_only_fields = ["id, created_at", "updated_at"]


class StockSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = Stock
        fields = ["id", "size", "quantity", "price", "profited_price", "discount"]
        read_only_fields = ["id"]


class ColorSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True)

    class Meta:
        model = Color
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


class FilterColorSerializer(ColorSerializer):
    class Meta(ColorSerializer.Meta):
        model = Color
        fields = ["id", "color1_name", "color1_value", "color2_name", "color2_value"]
        read_only_fields = ["id"]


class AdminColorsSerializer(serializers.ModelSerializer):
    """serializer for ProductColor model for admin control panel"""

    class Meta:
        model = Color
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class AdminStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
