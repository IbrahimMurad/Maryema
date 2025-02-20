from profile.models import Profile

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from core.permissions import IsAdminOrReadOnly


class IsAdminOrReadOnlyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="admin", password="admin", email="admin@test.com"
        )
        cls.customer = User.objects.create_user(
            username="customer", password="customer", email="customer@test.com"
        )
        cls.admin_profile = Profile.objects.create(
            user=cls.admin, role=Profile.RoleChoices.ADMIN
        )
        cls.customer_profile = Profile.objects.create(
            user=cls.customer, role=Profile.RoleChoices.CUSTOMER
        )
        cls.permission = IsAdminOrReadOnly()

    def setUp(self):
        self.factory = RequestFactory()

    def test_safe_method_allows_everyone(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()
        self.assertTrue(self.permission.has_permission(request, None))
        request.user = self.customer
        self.assertTrue(self.permission.has_permission(request, None))
        request.user = self.admin
        self.assertTrue(self.permission.has_permission(request, None))

    def test_non_safe_method_denies_anonymous(self):
        request = self.factory.post("/")
        request.user = AnonymousUser()
        self.assertFalse(self.permission.has_permission(request, None))

    def test_non_safe_method_denies_non_admin(self):
        request = self.factory.post("/")
        request.user = self.customer
        self.assertFalse(self.permission.has_permission(request, None))

    def test_non_safe_method_allows_admin(self):
        request = self.factory.post("/")
        request.user = self.admin
        self.assertTrue(self.permission.has_permission(request, None))
