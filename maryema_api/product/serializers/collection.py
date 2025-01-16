from rest_framework import serializers

from product.models import Collection, Product


class CollectionProductSerializer(serializers.ModelSerializer):
    """A serializer for product model specific to collection"""

    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", read_only=True
    )
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "url", "name", "description", "category"]
        read_only_fields = ["id"]


class ReadCollectionSerializer(serializers.ModelSerializer):
    """A serializer for collection model specific for read only actions"""

    url = serializers.HyperlinkedIdentityField(
        view_name="collection-detail", read_only=True
    )
    products = CollectionProductSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class WriteCollectionSerializer(serializers.ModelSerializer):
    """A serializer for collection model specific for write actions"""

    class Meta:
        model = Collection
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
