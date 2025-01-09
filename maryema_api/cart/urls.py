from django.urls import path

from cart.views import (
    AddToCartView,
    CheckoutView,
    ClearCartView,
    GetCartView,
    UpdateDeleteCartItemView,
)

urlpatterns = [
    path("", GetCartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path("clear/", ClearCartView.as_view(), name="clear-cart"),
    path(
        "item/<uuid:pk>/",
        UpdateDeleteCartItemView.as_view(),
        name="cart-item",
    ),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
