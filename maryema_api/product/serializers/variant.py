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


class ProductDetailVariantSerializer(serializers.ModelSerializer):
    """A serializer for ProductVariant model specific to product-detail public view"""

    color = NestedColorSerializer(read_only=True)
    size = NestedSizeSerializer(read_only=True)
    image = NestedImgSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        exclude = ["product"]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "cost",
            "price",
            "quantity",
            "sort_order",
        ]
