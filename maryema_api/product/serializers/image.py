from rest_framework import serializers

from product.models import Img


class ImgSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="img-detail", read_only=True)

    class Meta:
        model = Img
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class NestedImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        exclude = ["created_at", "updated_at"]
        read_only_fields = ["id"]
