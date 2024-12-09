from rest_framework import serializers

from discounts.models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"
        exclude = ["created_at", "updated_at"]
        read_only_fields = ["id"]
