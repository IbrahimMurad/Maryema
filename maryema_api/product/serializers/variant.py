from rest_framework import serializers

from product.models import ProductVariant
from product.serializers.color import NestedColorSerializer
from product.serializers.image import NestedImgSerializer
from product.serializers.size import NestedSizeSerializer


class VariantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="variant-detail",
        read_only=True,
    )
    wished_by = serializers.SerializerMethodField()

    def get_wished_by(self, obj):
        return obj.wished_by.count()

    class Meta:
        model = ProductVariant
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class NestedVariantSerializer(serializers.ModelSerializer):
    color = NestedColorSerializer()
    size = NestedSizeSerializer()
    image = NestedImgSerializer()

    class Meta:
        model = ProductVariant
        exclude = ["created_at", "updated_at", "product"]
        read_only_fields = [
            "id",
            "color",
            "size",
            "image",
            "cost",
            "price",
            "quantity",
            "sort_order",
        ]
