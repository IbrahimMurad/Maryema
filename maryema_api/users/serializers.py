from rest_framework import serializers

from users.models import User


class AdminSerializer(serializers.ModelSerializer):
    """Serializer for admin control over users
    ensures all the data (except the password) is validated and returned"""

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        del representation["password"]
        return representation

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one digit"
            )
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one letter"
            )
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter"
            )
        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter"
            )
        if not any(char in "!@#$%^&*()-_+=[]{}|\\:;\"'<>,.?/~`" for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one special character"
            )
        return value


class CustomerSerializer(AdminSerializer):
    """Serializer for customer profile view.
    It inherits from AdminSerializer to have all of its features.
    It only edits the fields that are allowed to be edited by the customer"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "avatar",
            "first_name",
            "last_name",
            "password",
        ]
