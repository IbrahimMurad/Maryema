from profile.views import ChangePassword, CurrentUserView

from django.urls import path

urlpatterns = [
    path("change-password/", ChangePassword.as_view(), name="change-password"),
    path("", CurrentUserView.as_view(), name="current-user"),
]
