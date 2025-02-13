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

    def run_validation(self, data):
        if "name" in data:
            data["name"] = " ".join(data["name"].split()).title()
        return super().run_validation(data)


class CategoryNestedSerializer(serializers.ModelSerializer):
    """A serializer for Category model specific to products list view"""

    url = serializers.HyperlinkedIdentityField(
        view_name="category-detail", read_only=True
    )

    class Meta:
        model = Category
        fields = ["id", "url", "name"]
        read_only_fields = ["id", "url", "name"]


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
