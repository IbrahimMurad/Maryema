from rest_framework import serializers

from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer"""

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "order"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="order-detail")

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "status",
            "total",
            "profile",
        ]
