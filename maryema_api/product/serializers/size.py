from rest_framework import serializers

from product.models import Size


class SizeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="size-detail", read_only=True)

    class Meta:
        model = Size
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
