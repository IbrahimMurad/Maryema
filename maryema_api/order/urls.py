from django.urls import path

from order.views import OrderItemView

urlpatterns = [
    path("item/<int:pk>/", OrderItemView.as_view(), name="order-item"),
]
