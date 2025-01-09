from profile.models import Profile

from django.contrib.auth.models import User
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    """
    A serializer for Profile model to use as a nested field in UserSerializer
    """

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["role", "phone_number", "avatar_url", "avatar", "note", "wishlist"]
        read_only_fields = ["avatar_url", "wishlist"]
        extra_kwargs = {
            "avatar": {"write_only": True},
        }

    def get_avatar_url(self, obj):
        if obj.avatar and not obj.avatar_url.startswith("http"):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.avatar_url)
        return obj.avatar_url


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for User model
    """

    url = serializers.HyperlinkedIdentityField(view_name="user-detail")
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "url",
            "date_joined",
            "last_login",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "profile",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["id", "date_joined", "last_login"]

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        profile = instance.profile

        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()

        if profile_data:
            profile.role = profile_data.get("role", profile.role)
            profile.phone_number = profile_data.get(
                "phone_number", profile.phone_number
            )
            profile.note = profile_data.get("note", profile.note)
        profile.save()

        return instance
