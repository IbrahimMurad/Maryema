from rest_framework import serializers

from cart.models import Cart, CartItem
from stock.models import Stock


class StockItemSerializer(serializers.ModelSerializer):
    """Stock item serializer for cart"""

    product_name = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    product_discount = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = [
            "id",
            "product_name",
            "color",
            "size",
            "price",
            "product_discount",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "color",
            "size",
            "price",
            "product_discount",
        ]

    def get_product_name(self, obj):
        return obj.product_colored.product.name

    def get_color(self, obj):
        return obj.product_colored.color1_name + (
            f"-{obj.product_colored.color2_name}"
            if obj.product_colored.color2_name
            else ""
        )

    def get_product_discount(self, obj):
        if obj.product_colored.product.discount:
            return obj.product_colored.product.discount.amount
        return 0


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "cart"]


class CartItemDetailsSerializer(serializers.ModelSerializer):
    product = StockItemSerializer()

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "cart"]


class CartSerializer(serializers.ModelSerializer):
    unique_items = serializers.SerializerMethodField()
    number_of_items = serializers.SerializerMethodField()
    items = CartItemDetailsSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "profile",
            "total",
            "unique_items",
            "number_of_items",
            "items",
        ]
        read_only_fields = ["profile", "status", "total_price", "total"]

    def get_unique_items(self, obj):
        return obj.items.count()

    def get_number_of_items(self, obj):
        return sum([item.quantity for item in obj.items.all()])
