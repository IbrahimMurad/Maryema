from rest_framework import serializers

from feedbacks.models import Feedback
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
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
