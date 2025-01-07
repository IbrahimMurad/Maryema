from rest_framework import serializers

from cart.models import Cart, CartItem


class CartItemSerrializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerrializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
