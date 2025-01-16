from rest_framework import serializers

from product.models import Category
from product.serializers.division import DivisionNestedSerializer


class CategorySerializer(serializers.ModelSerializer):
    """A serializer for Category model specific to admin"""

    url = serializers.HyperlinkedIdentityField(
        view_name="category-detail", read_only=True
    )

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class CategoryNestedSerializer(serializers.ModelSerializer):
    """A serializer for Category model specific to products list view"""

    url = serializers.HyperlinkedIdentityField(
        view_name="category-detail", read_only=True
    )

    class Meta:
        model = Category
        fields = ["id", "url", "name"]
        read_only_fields = ["id"]


class DivisionNestedCategorySerializer(serializers.ModelSerializer):
    """A serializer for Category model specific to product detail view"""

    url = serializers.HyperlinkedIdentityField(
        view_name="category-detail", read_only=True
    )
    division = DivisionNestedSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "url", "name", "division"]
        read_only_fields = ["id"]
