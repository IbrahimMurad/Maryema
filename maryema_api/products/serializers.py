from rest_framework import serializers

from products.models import Category, Division, Product
from stock.models import ProductColor, Stock


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    division = DivisionSerializer()

    class Meta:
        model = Category
        fields = ["id", "name", "division"]


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "size",
            "quantity",
            "selling_price",
        ]


class ProductColorSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True)

    class Meta:
        model = ProductColor
        fields = [
            "id",
            "color_1",
            "color_2",
            "image",
            "stocks",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_colored = ProductColorSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "product_colored",
        ]
        filterset_fields = ["category"]
