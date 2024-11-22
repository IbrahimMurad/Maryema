from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    AdminCustomersViewSet,
    ChangePassword,
    ProfileViewSet,
    UserAuthViewSet,
)

router = DefaultRouter()
router.register(r"admin/customers", AdminCustomersViewSet, basename="admin-customers")
router.register(r"auth", UserAuthViewSet, basename="auth")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "profile/change-password/",
        ChangePassword.as_view({"put": "change_password"}),
        name="change-password",
    ),
    path(
        "profile/",
        ProfileViewSet.as_view(
            {"get": "profile", "put": "profile", "delete": "profile"}
        ),
    ),
    path(
        "admin/customers/<int:pk>/",
        AdminCustomersViewSet.as_view(
            {"get": "customer", "put": "customer", "delete": "customer"}
        ),
    ),
]
