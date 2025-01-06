from profile.views import ChangePassword, CurrentUserView, api_root

from django.urls import path

urlpatterns = [
    path("me/change-password/", ChangePassword.as_view(), name="change-password"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("", api_root, name="api-root"),
]
