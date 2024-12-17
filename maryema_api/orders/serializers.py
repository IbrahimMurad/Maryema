from rest_framework import serializers

from cart.serializers import CartSerializer, StockItemSerializer
from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = StockItemSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "order"]


class OrderSerializer(CartSerializer):
    items = OrderItemSerializer(many=True)

    class Meta(CartSerializer.Meta):
        model = Order
