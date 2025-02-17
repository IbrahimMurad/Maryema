from profile.models import Profile

from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase

from core.utils import create_image
from product.models import Img
from product.tests.factories import ImgFactory


class ImgViewSetTestCase(APITestCase):
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
        cls.request = RequestFactory().get("/")

    def test_list_images(self) -> None:
        ImgFactory.create_batch(10)
        response = self.client.get("/api/imgs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)

    def test_retireive_image(self) -> None:
        img = ImgFactory()
        response = self.client.get(f"/api/imgs/{img.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["src"], self.request.build_absolute_uri(img.src.url)
        )
        self.assertEqual(response.data["alt"], img.alt)

    def test_create_new_img(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/imgs/",
            {
                "src": create_image(),
                "alt": "test",
            },
            format="multipart",
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Img.objects.count(), 1)
        self.assertEqual(response.data["alt"], "test")
        img = Img.objects.last()
        self.assertEqual(
            response.data["src"], self.request.build_absolute_uri(img.src.url)
        )

    def test_update_new_img(self) -> None:
        self.client.force_authenticate(user=self.admin)
        img = ImgFactory()
        response = self.client.put(
            f"/api/imgs/{img.pk}/",
            {"src": create_image(name="new_img.jpg"), "alt": "new alt"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        img.refresh_from_db()
        self.assertEqual(response.data["alt"], "new alt")
        self.assertEqual(
            response.data["src"], self.request.build_absolute_uri(img.src.url)
        )

    def test_partial_update_new_img(self) -> None:
        self.client.force_authenticate(user=self.admin)
        img = ImgFactory()
        response = self.client.patch(
            f"/api/imgs/{img.pk}/",
            {"alt": "new alt"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        img.refresh_from_db()
        self.assertEqual(response.data["alt"], "new alt")
        self.assertEqual(
            response.data["src"], self.request.build_absolute_uri(img.src.url)
        )

    def test_delete_img(self) -> None:
        self.client.force_authenticate(user=self.admin)
        img = ImgFactory()
        self.assertEqual(Img.objects.count(), 1)
        response = self.client.delete(f"/api/imgs/{img.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Img.objects.count(), 0)

    def test_unauthorized_create_img(self) -> None:
        # unauthenticated user
        response = self.client.post(
            "/api/imgs/",
            {
                "src": create_image(),
                "alt": "test",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Img.objects.count(), 0)

        # customer
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(
            "/api/imgs/",
            {
                "src": create_image(),
                "alt": "test",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Img.objects.count(), 0)

    def test_unauthorized_update_img(self) -> None:
        img = ImgFactory()
        # unauthenticated user
        response = self.client.put(
            f"/api/imgs/{img.pk}/",
            {"src": create_image(name="new_img.jpg"), "alt": "new alt"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        img.refresh_from_db()
        self.assertNotEqual(img.alt, "new alt")

        # customer
        self.client.force_authenticate(user=self.customer)
        response = self.client.put(
            f"/api/imgs/{img.pk}/",
            {"src": create_image(name="new_img.jpg"), "alt": "new alt"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        img.refresh_from_db()
        self.assertNotEqual(img.alt, "new alt")

    def test_unauthorized_partial_update_img(self) -> None:
        img = ImgFactory()
        # unauthenticated user
        response = self.client.patch(
            f"/api/imgs/{img.pk}/",
            {"alt": "new alt"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        img.refresh_from_db()
        self.assertNotEqual(img.alt, "new alt")

        # customer
        self.client.force_authenticate(user=self.customer)
        response = self.client.patch(
            f"/api/imgs/{img.pk}/",
            {"alt": "new alt"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        img.refresh_from_db()
        self.assertNotEqual(img.alt, "new alt")

    def test_unauthorized_delete(self) -> None:
        img = ImgFactory()
        # unauthenticated user
        response = self.client.delete(f"/api/imgs/{img.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Img.objects.count(), 1)

        # customer
        self.client.force_authenticate(user=self.customer)
        response = self.client.delete(f"/api/imgs/{img.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Img.objects.count(), 1)

    def test_create_img_with_no_file(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/imgs/",
            {
                "alt": "test",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Img.objects.count(), 0)
        self.assertEqual(response.data["src"][0], "No file was submitted.")

    def test_create_with_invalid_img(self) -> None:
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/imgs/",
            {
                "src": "awsome_image.jpg",  # this is just a string, not an image file
                "alt": "test",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Img.objects.count(), 0)
        self.assertEqual(response.data["src"][0].code, "invalid")
        self.assertEqual(
            str(response.data["src"][0]),
            "The submitted data was not a file. Check the encoding type on the form.",
        )

    def test_update_img_with_no_file(self) -> None:
        self.client.force_authenticate(user=self.admin)
        img = ImgFactory()
        old_alt = img.alt
        response = self.client.put(
            f"/api/imgs/{img.pk}/",
            {
                "alt": "test",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["src"][0], "No file was submitted.")
        img.refresh_from_db()
        self.assertEqual(img.alt, old_alt)

    def test_update_with_invalid_img(self) -> None:
        self.client.force_authenticate(user=self.admin)
        img = ImgFactory()
        old_src = img.src
        old_alt = img.alt
        response = self.client.patch(
            f"/api/imgs/{img.pk}/",
            {
                "src": "awsome_image.jpg",  # this is just a string, not an image file
                "alt": "test",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["src"][0].code, "invalid")
        self.assertEqual(
            str(response.data["src"][0]),
            "The submitted data was not a file. Check the encoding type on the form.",
        )
        img.refresh_from_db()
        self.assertEqual(img.src, old_src)
        self.assertEqual(img.alt, old_alt)
