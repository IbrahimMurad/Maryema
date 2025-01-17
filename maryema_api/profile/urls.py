from profile.views import (
    ChangePassword,
    CurrentUserView,
    Logout,
    ObtainToken,
    RefreshToken,
    Register,
)

from django.urls import path

urlpatterns = [
    path("change-password/", ChangePassword.as_view(), name="change-password"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("logout/", Logout.as_view(), name="logout"),
    path("login/", ObtainToken.as_view(), name="login"),
    path("refresh/", RefreshToken.as_view(), name="refresh"),
    path("register/", Register.as_view(), name="register"),
]
