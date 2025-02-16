from rest_framework import serializers

from product.models import Color


class ColorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="color-detail", read_only=True)

    class Meta:
        model = Color
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class NestedColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        exclude = ["created_at", "updated_at"]
        read_only_fields = [
            "id",
            "color1_name",
            "color1_value",
            "color2_name",
            "color2_value",
        ]
