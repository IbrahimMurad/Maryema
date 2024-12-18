from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "role",
            "avatar",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "is_active",
            "profile",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """override the default create method so that we can create the profile data
        since the profile data is nested in the user data
        and the default create data does not handle nested data"""
        print(validated_data)
        profile_data = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        """override the default update method so that we can update the profile data
        since the profile data is nested in the user data
        and the default update data does not handle nested data"""

        profile_data = validated_data.pop("profile", None)
        profile = instance.profile

        for attr, value in validated_data.items():
            # handle password separatly since it is hashed
            if attr != "password":
                setattr(instance, attr, value)
            else:
                instance.set_password(value)
        instance.save()

        if profile_data:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance
