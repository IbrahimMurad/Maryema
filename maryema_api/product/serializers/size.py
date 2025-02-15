from rest_framework import serializers

from product.models import Size


class SizeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="size-detail", read_only=True)

    class Meta:
        model = Size
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def run_validation(self, data):
        """Converts the name field to uppercase and removes extra whitespaces"""
        data = data.copy()
        if "name" in data:
            data["name"] = "".join(data["name"].split()).upper()
        return super().run_validation(data)


class NestedSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        exclude = ["created_at", "updated_at"]
        read_only_fields = ["id", "name"]
