from rest_framework import serializers

from feedbacks.models import Feedback
from products.models import Product
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model"""

    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "avatar", "username"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_username(self, obj):
        return obj.user.username


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for the Feedback model"""

    customer = ProfileSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = [
            "id",
            "rate",
            "comment",
            "customer",
            "product",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["customer"] = self.context["request"].user.profile
        product_id = self.context["request"].parser_context["kwargs"]["product_pk"]
        validated_data["product"] = Product.objects.get(id=product_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["customer"] = self.context["request"].user.profile
        product_id = self.context["request"].parser_context["kwargs"]["product_pk"]
        validated_data["product"] = Product.objects.get(id=product_id)
        return super().update(instance, validated_data)
