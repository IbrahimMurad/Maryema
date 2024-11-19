from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminCustomersViewSet, ProfileViewSet, UserAuthViewSet

router = DefaultRouter()
router.register(r"admin/customers", AdminCustomersViewSet, basename="admin-customers")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"auth", UserAuthViewSet, basename="auth")

urlpatterns = [
    path("", include(router.urls)),
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
