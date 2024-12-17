from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Order.StatusChoice.CANCELED
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def reorder(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Order.StatusChoice.PENDING
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
