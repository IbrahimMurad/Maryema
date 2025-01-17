"""
URL configuration for core project.
"""

from profile.views import UserViewSet

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.drf_yasg import urlpatterns as open_api_urls
from feedback.views import FeedbackViewSet
from order.views import OrderViewSet
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
router.register("feedback", FeedbackViewSet, basename="feedback")
router.register("orders", OrderViewSet, basename="order")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/cart/", include("cart.urls")),
    path("api/order/", include("order.urls")),
    path("api/auth/", include("profile.urls")),
    path("api/", include(router.urls)),
]


urlpatterns += open_api_urls

if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
