from profile.models import Profile

from django.db.models import Sum
from rest_framework import serializers

from feedback.serializers import FeedbackSerializer
from product.models import Product
from product.serializers.category import CategoryNestedSerializer
from product.serializers.variant import ProductDetailVariantSerializer


class ProductSerializer(serializers.ModelSerializer):
    """A serializer for Product model specific to admin"""

    url = serializers.HyperlinkedIdentityField(
        view_name="admin-product-detail", read_only=True
    )
    feedback = FeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        if attrs.get("provider") is not None:
            if attrs.get("provider").role != Profile.RoleChoices.PROVIDER:
                raise serializers.ValidationError(
                    {"provider": "Only providers can provide products"}
                )
        return super().validate(attrs)


class ProductListPublicSerializer(serializers.ModelSerializer):
    """A serializer for Product model specific to public and for list action"""

    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", read_only=True
    )
    category = CategoryNestedSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["provider"]
        read_only_fields = ["id", "created_at", "updated_at", "category"]

    def get_image(self, obj):
        return obj.variants.get(sort_order=1).image.src.url

    def get_price(self, obj):
        return obj.variants.get(sort_order=1).price

    def get_in_stock(self, obj):
        return obj.variants.all().aggregate(in_stock=Sum("quantity"))["in_stock"]


class ProductDetailPublicSerializer(ProductListPublicSerializer):
    """A serializer for Product model specific to public and for retrieve action"""

    feedback = FeedbackSerializer(many=True, read_only=True)
    variants = ProductDetailVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ["provider"]
        read_only_fields = ["id", "created_at", "updated_at", "category"]
