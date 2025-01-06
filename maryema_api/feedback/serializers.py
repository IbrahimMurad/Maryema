from rest_framework import serializers

from feedback.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "product", "customer"]

    def validate(self, attrs):
        request = self.context.get("request")
        if request.method == "POST":
            customer = request.user.profile
            if not customer:
                raise serializers.ValidationError({"customer": "Customer is required."})
            if customer.role != "customer":
                raise serializers.ValidationError(
                    {"customer": "Only customers can leave feedback."}
                )
            attrs["customer"] = customer

        return super().validate(attrs)
