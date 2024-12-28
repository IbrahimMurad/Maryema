from io import BytesIO
from profile.models import Profile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image


def create_image(
    name: str = "default.png", size: tuple[int, int] = (100, 100)
) -> SimpleUploadedFile:
    file: BytesIO = BytesIO()
    image: Image.Image = Image.new("RGB", size=size)
    image.save(file, "png")
    file.name = name
    file.seek(0)
    return SimpleUploadedFile(
        name=file.name, content=file.read(), content_type="image/png"
    )


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="TestUser",
            email="user@test.com",
            password="password",
            first_name="Test",
            last_name="User",
        )

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(), 0)
        Profile.objects.create(user=self.user)
        self.assertEqual(Profile.objects.count(), 1)

    def test_profile_str(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), self.user.username)

    def test_profile_default_role(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.role, Profile.RoleChoices.CUSTOMER)

    def test_profile_default_phone_number(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.phone_number, "")

    def test_profile_default_avatar(self):
        profile = Profile.objects.create(user=self.user)
        self.assertFalse(profile.avatar)
        self.assertEqual(
            profile.avatar_url,
            f"https://avatar.iran.liara.run/public/{51 + (int(profile.id) % 50)}",
        )

    def test_profile_default_note(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.note, "")

    def test_profile_role(self):
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(profile.is_customer)
        self.assertFalse(profile.is_admin)
        self.assertFalse(profile.is_provider)

        profile.role = Profile.RoleChoices.ADMIN
        profile.save()
        self.assertTrue(profile.is_admin)
        self.assertFalse(profile.is_customer)
        self.assertFalse(profile.is_provider)

        profile.role = Profile.RoleChoices.PROVIDER
        profile.save()
        self.assertTrue(profile.is_provider)
        self.assertFalse(profile.is_customer)
        self.assertFalse(profile.is_admin)

    def test_profile_with_role_outside_choices(self):
        profile = Profile(user=self.user, role="invalid")
        with self.assertRaises(ValidationError):
            profile.save()

    def test_phone_number_max_length(self):
        profile = Profile(user=self.user, phone_number="1234567890123456")
        with self.assertRaises(ValidationError):
            profile.save()

    def test_profile_required_user(self):
        profile = Profile()
        with self.assertRaises(ValidationError):
            profile.save()

    def test_user_cascade_delete(self):
        Profile.objects.create(user=self.user)
        self.assertEqual(Profile.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Profile.objects.count(), 0)

    def test_profile_avatar(self):
        profile = Profile.objects.create(user=self.user, avatar=create_image())
        self.assertEqual(profile.avatar_url, profile.avatar.url)
        self.assertRegex(profile.avatar.name, r"^avatars\/default(_\S*)?.png")
        self.assertRegex(profile.avatar.url, r"^\/media\/avatars\/default(_\S*)?.png")
