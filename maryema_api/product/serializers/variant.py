from django.urls import reverse
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
    wished_by = serializers.SerializerMethodField()

    def get_wished_by(self, obj):
        request = self.context.get("request")
        return [
            request.build_absolute_uri(reverse("user-detail", args=[profile.user.id]))
            for profile in obj.wished_by.all()
        ]

    class Meta:
        model = ProductVariant
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        depth = 1


class ProductDetailVariantSerializer(serializers.ModelSerializer):
    """A serializer for ProductVariant model specific to product-detail public view"""

    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    image = ImgSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        exclude = ["product"]
        read_only_fields = ["id", "created_at", "updated_at"]
