from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a new user.
        """
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Update a user.
        """
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model for admin control over customers.
    """

    class Meta:
        model = User
        exclude = ["password"]
        read_only_fields = [
            "id",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        ]

    def update(self, instance, validated_data):
        """
        Update a user.
        """
        user = super().update(instance, validated_data)
        return user
