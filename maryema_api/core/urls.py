"""
URL configuration for core project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from products.views import CategoryViewSet, DivisionViewSet, ProductViewSet
from stock.views import ProductColorViewSet, SizeViewSet, StockViewSet

router = routers.DefaultRouter()
router.register(r"stocks", StockViewSet)
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"divisions", DivisionViewSet)
router.register(r"sizes", SizeViewSet)
router.register(r"product-colors", ProductColorViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
