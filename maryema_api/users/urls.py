from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    AdminUsersView,
    CustomerProfileView,
    LogInView,
    LogOutView,
    RegisterUserView,
)

router = DefaultRouter()
router.register("users", AdminUsersView)

urlpatterns = [
    path("admin/", include(router.urls)),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("profile/", CustomerProfileView.as_view(), name="profile"),
]
