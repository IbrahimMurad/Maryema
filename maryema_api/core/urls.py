"""
URL configuration for core project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from feedbacks.views import FeedbackViewSet
from products.views import FilterDataView, ProductDetailsViewSet, ProductViewSet
from users.views import CustomerViewSet, UsersViewSet

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")
router.register("customers", CustomerViewSet, basename="customers")
router.register("products", ProductViewSet, basename="products")
router.register("product-details", ProductDetailsViewSet, basename="product-details")
router.register("feedbacks", FeedbackViewSet, basename="feedbacks")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/filter/", FilterDataView.as_view(), name="filter"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
