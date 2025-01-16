from rest_framework import serializers

from product.models import ProductVariant
from product.serializers.color import ColorSerializer
from product.serializers.image import ImgSerializer
from product.serializers.size import SizeSerializer


class VariantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="variant-detail",
        read_only=True,
    )

    class Meta:
        model = ProductVariant
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request.user.is_authenticated and request.user.profile.is_admin:
            fields.update(
                {
                    "wished_by": serializers.PrimaryKeyRelatedField(
                        many=True, read_only=True, allow_empty=True
                    )
                }
            )
        return fields


class writeVariantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="variant-detail", read_only=True
    )

    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductDetailVariantSerializer(serializers.ModelSerializer):
    """A serializer for ProductVariant model specific to product-detail public view"""

    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    image = ImgSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        exclude = ["product"]
        read_only_fields = ["id", "created_at", "updated_at"]
