from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdmin, IsOwner
from order.models import Order, OrderItem
from order.permissions import IsAdminOrOwner
from order.serializers import OrderItemSerializer, OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["item__product_variant__product__name"]
    filterset_fields = ["status"]

    def get_queryset(self):
        """
        return all orders if the user is an admin otherwise return only the orders of the user
        """
        if self.request.user.profile.role == "admin":
            return Order.objects.all()
        return Order.objects.filter(profile=self.request.user.profile)

    def create(self, request):
        """
        Create a new order
        """
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                profile=request.user.profile, status=Order.StatusChoice.PENDING
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def close(self, request, pk=None):
        """
        Close the order
        """
        order = self.get_object()
        order.status = Order.StatusChoice.CLOSED
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"], permission_classes=[IsOwner])
    def cancel(self, request, pk=None):
        """
        Cancel the order
        """
        order = self.get_object()
        order.cancel_reason = request.data.get("cancel_reason", "")
        order.status = Order.StatusChoice.CANCELED
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def process(self, request, pk=None):
        """
        Change the status of the order to processing
        """
        order = self.get_object()
        order.status = Order.StatusChoice.PROCESSING
        order.save()
        return Response(OrderSerializer(order).data)

    @action(
        detail=True, methods=["post"], permission_classes=[IsAdmin], url_path="add-item"
    )
    def add_item(self, request, pk=None):
        """
        Add an item to the order
        """
        order = self.get_object()
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            order.items.create(**serializer.validated_data)
            return Response(OrderSerializer(order).data)
        return Response(serializer.errors, status=400)


class OrderItemView(views.APIView):
    def patch(self, request, pk=None):
        if request.user.profile.role != "admin":
            return Response(
                {"error": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        order_item = OrderItem.objects.get(pk=pk)
        serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        if request.user.profile.role != "admin":
            return Response(
                {"error": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        order_item = OrderItem.objects.get(pk=pk)
        order_item.delete()
        return Response(status=204)
