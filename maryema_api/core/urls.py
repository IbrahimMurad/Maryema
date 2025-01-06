"""
URL configuration for core project.
"""

from profile.views import UserViewSet

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from product.views import (
    CategoryViewSet,
    CollectionViewSet,
    ColorViewSet,
    DivisionViewSet,
    ImgViewSet,
    ProductViewSet,
    SizeViewSet,
    VariantViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("divisions", DivisionViewSet, basename="division")
router.register("categories", CategoryViewSet, basename="category")
router.register("colors", ColorViewSet, basename="color")
router.register("sizes", SizeViewSet, basename="size")
router.register("imgs", ImgViewSet, basename="img")
router.register("products", ProductViewSet, basename="product")
router.register("variants", VariantViewSet, basename="variant")
router.register("collections", CollectionViewSet, basename="collection")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/admin/", include(router.urls)),
    path("api/", include("profile.urls")),
]

if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
