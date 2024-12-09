from rest_framework import serializers

from feedbacks.serializers import FeedbackSerializer
from products.models import Category, Division, Product
from stock.serializers import ProductColorSerializer


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ["id", "name"]
        read_only_fields = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    division = DivisionSerializer()

    class Meta:
        model = Category
        fields = ["id", "name", "division"]
        read_only_fields = ["id"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Serializer for Category model for product detail view"""

    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id"]

    def get_price(self, obj):
        return obj.price

    def get_image(self, obj):
        return obj.image


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer()
    colors = ProductColorSerializer(many=True)
    feedbacks = FeedbackSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "colors",
            "image",
            "feedbacks",
        ]
        read_only_fields = ["id"]
