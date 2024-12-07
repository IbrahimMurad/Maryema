from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profile


class ProfileSerialiser(serializers.ModelSerializer):
    """
    Serializer for the User model for customers.
    """

    class Meta:
        model = Profile
        fields = ["avatar", "phone_number"]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model for customers.
    """

    profile = ProfileSerialiser()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "profile",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        profile = instance.profile

        # Update profile fields
        for attr, value in profile_data.items():
            current_value = getattr(profile, attr)
            if current_value != value:
                setattr(profile, attr, value)
        profile.save()

        # Update User fields
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance
