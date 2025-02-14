from profile.models import Profile

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from product.models import Division


class DivisionViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin = User.objects.create_user(
            username="TestAdmin",
            email="admin@test.com",
            password="admin_password",
            first_name="Test",
            last_name="Admin",
        )
        cls.customer = User.objects.create_user(
            username="TestCustomer",
            email="customer@test.com",
            password="customer_password",
            first_name="Test",
            last_name="Customer",
        )
        cls.admin_profile = Profile.objects.create(
            user=cls.admin, role=Profile.RoleChoices.ADMIN
        )
        cls.customer_profile = Profile.objects.create(
            user=cls.customer, role=Profile.RoleChoices.CUSTOMER
        )
        cls.cloths = Division.objects.create(name="Clothes")
        cls.accessories = Division.objects.create(name="Accessories")
        cls.url = reverse("division-list")

    def test_list_divisions(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 2)
        self.assertEqual(response.data.get("results")[0].get("name"), "Accessories")

    def test_create_division(self) -> None:
        data = {"name": "Shoes"}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Division.objects.count(), 3)
        self.assertEqual(Division.objects.last().name, "Shoes")

    def test_retrieve_division(self) -> None:
        response = self.client.get(reverse("division-detail", args=[self.cloths.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Clothes")

    def test_partially_update_division(self) -> None:
        data = {"name": "Footwear"}
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("division-detail", args=[self.accessories.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.accessories.refresh_from_db()
        self.assertEqual(self.accessories.name, "Footwear")

    def test_update_division(self) -> None:
        data = {"name": "Footwear"}
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            reverse("division-detail", args=[self.accessories.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.accessories.refresh_from_db()
        self.assertEqual(self.accessories.name, "Footwear")

    def test_delete_division(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("division-detail", args=[self.cloths.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Division.objects.count(), 1)
        self.assertEqual(Division.objects.last().name, "Accessories")

    def test_unauthorized_create_division(self) -> None:
        data = {"name": "Shoes"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(user=self.customer)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update_division(self) -> None:
        data = {"name": "Footwear"}
        response = self.client.patch(
            reverse("division-detail", args=[self.accessories.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(user=self.customer)
        response = self.client.patch(
            reverse("division-detail", args=[self.accessories.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete_division(self) -> None:
        response = self.client.delete(reverse("division-detail", args=[self.cloths.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(user=self.customer)
        response = self.client.delete(reverse("division-detail", args=[self.cloths.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_division_url(self) -> None:
        response = self.client.get(self.url)
        clothes_url = response.data.get("results")[1].get("url")
        response = self.client.get(clothes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Clothes")
        self.assertEqual(response.data.get("url"), clothes_url)

    def test_create_division_blank_name(self) -> None:
        data = {"name": ""}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Division.objects.count(), 2)
        self.assertEqual(
            str(response.data.get("name")[0]), "This field may not be blank."
        )

    def test_create_division_duplicate_name(self) -> None:
        data = {"name": "Shoes"}
        self.client.force_authenticate(user=self.admin)

        # create the first division
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try to create the dublicate
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Division.objects.count(), 3)
        self.assertEqual(
            str(response.data.get("name")[0]),
            "Division with this name already exists.",
        )
