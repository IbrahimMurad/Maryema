from profile.models import Profile

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from product.models import Category, Division


class DivisionViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Set up objects once for the test class
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
        cls.shirts = Category.objects.create(name="Shirts", division=cls.cloths)
        cls.pants = Category.objects.create(name="Pants", division=cls.cloths)
        cls.hoodies = Category.objects.create(name="Hoodies", division=cls.cloths)
        cls.shoes = Category.objects.create(name="Shoes", division=cls.accessories)
        cls.bags = Category.objects.create(name="Bags", division=cls.accessories)

    def test_list_categories(self) -> None:
        response = self.client.get(reverse("category-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 5)
        self.assertEqual(response.data.get("results")[0].get("name"), "Bags")

    def test_create_category(self) -> None:
        data = {"name": "socks", "division": self.accessories.pk}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 6)

    def test_retrieve_category(self) -> None:
        response = self.client.get(reverse("category-detail", args=[self.pants.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Pants")

    def test_partially_update_category(self) -> None:
        data = {"name": "Footwear"}
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("category-detail", args=[self.pants.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pants.refresh_from_db()
        self.assertEqual(self.pants.name, "Footwear")

    def test_update_category(self) -> None:
        data = {"name": "Footwear", "division": self.accessories.pk}
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            reverse("category-detail", args=[self.pants.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pants.refresh_from_db()
        self.assertEqual(self.pants.name, "Footwear")
        self.assertEqual(self.pants.division, self.accessories)

    def test_update_category_with_missing_field(self) -> None:
        data = {"name": "Footwear"}
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            reverse("category-detail", args=[self.pants.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("division"), ["This field is required."])

    def test_delete_category(self) -> None:
        self.client.force_authenticate(user=self.admin)
        self.assertIn(self.shirts, Category.objects.all())
        response = self.client.delete(reverse("category-detail", args=[self.shirts.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 4)
        self.assertNotIn(self.shirts, Category.objects.all())

    def test_unauthorized_create_category(self) -> None:
        data = {"name": "socks", "division": self.accessories.pk}
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_partial_update_category(self) -> None:
        data = {"name": "Footwear"}
        response = self.client.patch(
            reverse("category-detail", args=[self.pants.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(
            reverse("category-detail", args=[self.pants.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update_category(self) -> None:
        data = {"name": "socks", "division": self.accessories.pk}
        response = self.client.put(
            reverse("category-detail", args=[self.pants.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.customer)
        response = self.client.put(
            reverse("category-detail", args=[self.pants.pk]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete_category(self) -> None:
        response = self.client.delete(reverse("category-detail", args=[self.pants.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.customer)
        response = self.client.delete(reverse("category-detail", args=[self.pants.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_url(self) -> None:
        response = self.client.get(reverse("category-list"))
        bags_url = response.data.get("results")[0].get("url")
        response = self.client.get(bags_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Bags")
        self.assertEqual(response.data.get("url"), bags_url)

    def test_404_not_found(self) -> None:
        response = self.client.get(reverse("category-detail", args=[1000]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # 403 comes before 404, so login first to test 404
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse("category-detail", args=[self.accessories.id])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.put(
            reverse("category-detail", args=[self.accessories.id])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(
            reverse("category-detail", args=[self.accessories.id])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_category_missing_division(self) -> None:
        data = {"name": "socks"}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("division"), ["This field is required."])

    def test_create_category_blank_name(self) -> None:
        data = {"name": "", "division": self.accessories.pk}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("name")[0], "This field may not be blank.")

    def test_create_category_invalid_division_id(self) -> None:
        data = {"name": "socks", "division": 1000}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("division")[0],
            "“1000” is not a valid UUID.",
        )

    def test_create_category_nonexistent_division(self) -> None:
        data = {
            "name": "sun glasses",
            "division": self.pants.pk,  # pants is not a division
        }
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("division")[0],
            f'Invalid pk "{self.pants.pk}" - object does not exist.',
        )

    def test_create_category_missing_name(self) -> None:
        data = {"division": self.cloths.pk}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("name")[0], "This field is required.")

    def test_create_category_duplicate_name(self) -> None:
        data = {"name": "socks", "division": self.cloths.pk}
        self.client.force_authenticate(user=self.admin)
        # Create first category
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Try to create duplicate
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("name")[0], "Category with this name already exists."
        )
        self.assertEqual(Category.objects.count(), 6)
