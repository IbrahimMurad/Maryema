from rest_framework import serializers

from product.models import Division


class DivisionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="division-detail")

    class Meta:
        model = Division
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class DivisionNestedSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="division-detail")

    class Meta:
        model = Division
        fields = ["id", "url", "name"]
        read_only_fields = ["id"]
