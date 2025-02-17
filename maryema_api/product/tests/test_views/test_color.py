from profile.models import Profile

from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Color
from product.serializers import ColorSerializer
from product.tests.factories import ColorFactory


class ColorViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.color = ColorFactory.create_batch(3)
        cls.request = RequestFactory().get("/")
        cls.color_data = ColorSerializer(
            Color.objects.all(), many=True, context={"request": cls.request}
        ).data
        cls.list_url = reverse("color-list")
        cls.detail_url = reverse("color-detail", args=[cls.color_data[0]["id"]])
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

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data["results"], self.color_data)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.color_data[0])

    def test_retrieve_by_url_in_list(self):
        response = self.client.get(self.list_url)
        response = self.client.get(response.data["results"][0]["url"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.color_data[0])

    def test_create(self):
        self.client.force_authenticate(user=self.admin)
        data = {"color1_name": "Red", "color1_value": "#FF0000"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Color.objects.count(), 4)

    def test_update(self):
        self.client.force_authenticate(user=self.admin)
        data = {"color1_name": "Red", "color1_value": "#FF0000"}
        response = self.client.put(self.detail_url, data)
        color = Color.objects.get(**data)
        serializer = ColorSerializer(color, context={"request": self.request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update(self):
        self.client.force_authenticate(user=self.admin)
        data = {"color2_name": "Green", "color2_value": "#00FF00"}
        response = self.client.patch(self.detail_url, data)
        color = Color.objects.get(**data)
        serializer = ColorSerializer(color, context={"request": self.request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Color.objects.count(), 2)

    def test_unauthorized_create(self):
        data = {"color1_name": "Red", "color1_value": "#FF0000"}

        # unauthenticated
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # customer (not admin)
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        data = {"color1_name": "Red", "color1_value": "#FF0000"}

        # unauthenticated
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # customer (not admin)
        self.client.force_authenticate(user=self.customer)
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_partial_update(self):
        data = {"color2_name": "Green", "color2_value": "#00FF00"}

        # unauthenticated
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # customer (not admin)
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        # unauthenticated
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # customer (not admin)
        self.client.force_authenticate(user=self.customer)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_color_value(self):
        self.client.force_authenticate(user=self.admin)
        data = {"color1_name": "Red", "color1_value": "FF0000"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["color1_value"][0],
            "This is not a valid color",
        )

    def test_missing_color1_name(self):
        self.client.force_authenticate(user=self.admin)
        data = {"color1_value": "#FF0000"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["color1_name"][0]),
            "This field is required.",
        )

    def test_pagination(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(len(response.data["results"]), 3)

        ColorFactory.create_batch(10)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 13)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(len(response.data["results"]), 10)

        response = self.client.get(response.data["next"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 13)
        self.assertIsNone(response.data["next"])
        self.assertIsNotNone(response.data["previous"])
        self.assertEqual(len(response.data["results"]), 3)
