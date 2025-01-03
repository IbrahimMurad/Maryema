from profile.views import ChangePassword, CurrentUserView, UserViewSet, api_root

from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")


urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", include(router.urls)),
    path("me/change-password/", ChangePassword.as_view(), name="change-password"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
]
