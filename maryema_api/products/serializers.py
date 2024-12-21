from rest_framework import serializers

from products.models import Category, Division, Product
from stock.serializers import ColorSerializer


class DivisionSerializer(serializers.ModelSerializer):
    """Serializer for Division model for product detail view"""

    class Meta:
        model = Division
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model for product detail view"""

    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryListSerializer(serializers.ModelSerializer):
    """Serializer for Category model for admin control panel"""

    class Meta:
        model = Category
        fields = ["id", "name", "division"]


class ProductSerializer(serializers.ModelSerializer):
    display_price = serializers.SerializerMethodField(read_only=True)
    display_image = serializers.SerializerMethodField(read_only=True)
    average_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        exclude = ["updated_at"]
        read_only_fields = ["id"]

    def get_display_price(self, obj):
        return obj.display_price

    def get_display_image(self, obj):
        return obj.display_image

    def get_average_rate(self, obj):
        return obj.average_rate


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    colors = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "colors",
        ]
        read_only_fields = ["id"]


class AdminProductSerlaizer(serializers.ModelSerializer):
    """serializer for product model for admin control panel"""

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
