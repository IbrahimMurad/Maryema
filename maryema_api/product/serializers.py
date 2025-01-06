from profile.models import Profile

from rest_framework import serializers

from product.models import (
    Category,
    Collection,
    Color,
    Division,
    Img,
    Product,
    ProductVariant,
    Size,
)


class DivisionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="division-detail")

    class Meta:
        model = Division
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="category-detail", read_only=True
    )

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ColorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="color-detail", read_only=True)

    class Meta:
        model = Color
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class SizeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="size-detail", read_only=True)

    class Meta:
        model = Size
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ImgSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="img-detail", read_only=True)

    class Meta:
        model = Img
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", read_only=True
    )

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


class VariantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="variant-detail", read_only=True
    )

    class Meta:
        model = ProductVariant
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class writeVariantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="variant-detail", read_only=True
    )
    size = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    image = ImgSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = "__all__"


class CollectionProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", read_only=True
    )
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "url", "name", "description", "category"]
        read_only_fields = ["id"]


class ReadCollectionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="collection-detail", read_only=True
    )
    products = CollectionProductSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class WriteCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
