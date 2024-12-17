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
from products.views import FilterDataView, ProductViewSet
from users.views import CustomerViewSet, UsersViewSet

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")
router.register("customers", CustomerViewSet, basename="customers")
router.register("products", ProductViewSet, basename="products")
router.register("carts", CartViewSet, basename="carts")
router.register("checkout", CheckoutView, basename="checkout")
router.register("orders", OrderViewSet, basename="orders")

# Create a nested router for feedbacks
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("feedbacks", FeedbackViewSet, basename="product-feedbacks")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(products_router.urls)),  # Include the nested router URLs
    path("api/filter/", FilterDataView.as_view(), name="filter"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
