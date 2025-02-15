from profile.models import Profile

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Size


class SizeViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="admin", password="admin", email="admin@test.com"
        )
        cls.admin_profile = Profile.objects.create(
            user=cls.admin, role=Profile.RoleChoices.ADMIN
        )
        cls.customer = User.objects.create_user(
            username="customer", password="customer", email="customer@test.com"
        )
        cls.customer_profile = Profile.objects.create(
            user=cls.customer, role=Profile.RoleChoices.CUSTOMER
        )
        cls.s_size = Size.objects.create(name="S")
        cls.m_size = Size.objects.create(name="M")
        cls.l_size = Size.objects.create(name="L")
        cls.xl_size = Size.objects.create(name="XL")
        cls.xxl_size = Size.objects.create(name="XXL")
        cls.size_14 = Size.objects.create(name="14")
        cls.size_16 = Size.objects.create(name="16")
        cls.size_32 = Size.objects.create(name="32")

    def test_list(self):
        response = self.client.get("/api/sizes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 8)
        self.assertEqual(response.data["results"][0]["name"], "S")

    def test_retrieve(self):
        response = self.client.get(f"/api/sizes/{self.s_size.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "S")

    def test_create(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/sizes/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "XS")
        self.assertEqual(Size.objects.count(), 9)
        self.assertEqual(Size.objects.last().name, "XS")

    def test_unauthorized_create(self):
        response = self.client.post("/api/sizes/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Size.objects.count(), 8)

        self.client.force_authenticate(user=self.customer)
        response = self.client.post("/api/sizes/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Size.objects.count(), 8)

    def test_update(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(f"/api/sizes/{self.s_size.pk}/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "XS")
        self.assertEqual(Size.objects.count(), 8)
        self.assertEqual(Size.objects.get(pk=self.s_size.pk).name, "XS")

    def test_unauthorized_update(self):
        response = self.client.put(f"/api/sizes/{self.s_size.pk}/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Size.objects.get(pk=self.s_size.pk).name, "S")

        self.client.force_authenticate(user=self.customer)
        response = self.client.put(f"/api/sizes/{self.s_size.pk}/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Size.objects.get(pk=self.s_size.pk).name, "S")

    def test_partial_update(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(f"/api/sizes/{self.s_size.pk}/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "XS")
        self.assertEqual(Size.objects.count(), 8)
        self.assertEqual(Size.objects.get(pk=self.s_size.pk).name, "XS")

    def test_unauthorized_partial_update(self):
        response = self.client.patch(f"/api/sizes/{self.s_size.pk}/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Size.objects.get(pk=self.s_size.pk).name, "S")

        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(f"/api/sizes/{self.s_size.pk}/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Size.objects.get(pk=self.s_size.pk).name, "S")

    def test_delete(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/sizes/{self.s_size.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Size.objects.count(), 7)

    def test_unauthorized_delete(self):
        response = self.client.delete(f"/api/sizes/{self.s_size.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Size.objects.count(), 8)

        self.client.force_authenticate(user=self.customer)
        response = self.client.delete(f"/api/sizes/{self.s_size.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Size.objects.count(), 8)

    def test_dublicate_size_name(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/sizes/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "XS")

        response = self.client.post("/api/sizes/", {"name": "XS"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["name"][0]), "Size with this name already exists."
        )
        self.assertEqual(Size.objects.count(), 9)

    def test_invalid_size_name(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/sizes/", {"name": "Small"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["name"][0]), "This is not a valid size")
        self.assertEqual(Size.objects.count(), 8)

    def test_pagination(self):
        response = self.client.get("/api/sizes/?page=2")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        Size.objects.create(name="XS")
        Size.objects.create(name="20")
        Size.objects.create(name="22")
        Size.objects.create(name="24")

        response = self.client.get("/api/sizes/?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(response.data["results"][0]["name"], "22")
        self.assertEqual(response.data["results"][1]["name"], "24")
        self.assertEqual(response.data["previous"], "http://testserver/api/sizes/")
