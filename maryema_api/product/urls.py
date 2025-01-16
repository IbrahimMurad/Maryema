from django.urls import path

from product.views import ProductPublicList, ProductPuplicRetrieve

urlpatterns = [
    path("", ProductPublicList.as_view(), name="product-list"),
    path("<uuid:pk>/", ProductPuplicRetrieve.as_view(), name="product-detail"),
]
