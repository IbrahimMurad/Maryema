"""
URL configuration for core project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from cart.views import CartViewSet, CheckoutView
from feedbacks.views import FeedbackViewSet
from orders.views import OrderViewSet
from products.views import (
    AdminProducViewset,
    CategoryViewSet,
    DivisionViewSet,
    FilterDataView,
    ProductViewSet,
)
from stock.views import AdminProductColorViewSet, AdminStockViewset, SizeViewSet
from users.views import AdminUsersViewSet, UsersViewSet

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")
router.register("products", ProductViewSet, basename="products")
router.register("carts", CartViewSet, basename="carts")
router.register("checkout", CheckoutView, basename="checkout")
router.register("orders", OrderViewSet, basename="orders")

# Create a nested router for feedbacks
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("feedbacks", FeedbackViewSet, basename="product-feedbacks")

admin_router = DefaultRouter()
admin_router.register("users", AdminUsersViewSet, basename="admin-users")
admin_router.register("divisions", DivisionViewSet, basename="divisions")
admin_router.register("categories", CategoryViewSet, basename="categories")
admin_router.register("products", AdminProducViewset, basename="admin-products")
admin_router.register("sizes", SizeViewSet, basename="sizes")

# nested router for product colors
admin_products_router = routers.NestedDefaultRouter(
    admin_router, "products", lookup="product"
)
admin_products_router.register(
    "colors", AdminProductColorViewSet, basename="product-colors"
)

# nested router for product stocks
stock_router = routers.NestedDefaultRouter(
    admin_products_router, "colors", lookup="color"
)
stock_router.register("stocks", AdminStockViewset, basename="product-stocks")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(products_router.urls)),
    path("api/admin/", include(admin_router.urls)),
    path("api/admin/", include(admin_products_router.urls)),
    path("api/admin/", include(stock_router.urls)),
    path("api/filter/", FilterDataView.as_view(), name="filter"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
