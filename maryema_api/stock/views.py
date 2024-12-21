from rest_framework import response, status, viewsets

from stock.models import Color, Size, Stock
from stock.serializers import (
    AdminColorsSerializer,
    AdminStockSerializer,
    ColorSerializer,
    SizeSerializer,
    StockSerializer,
)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ProductColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class AdminProductColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = AdminColorsSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_pk"]
        return super().get_queryset().filter(product__id=product_id)

    def create(self, request, *args, **kwargs):
        """override create to get the product id from the url"""
        data = request.data.copy()
        data["product"] = kwargs["product_pk"]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """override update to get the product id from the url"""
        instance = self.get_object()
        data = request.data.copy()
        data["product"] = kwargs["product_pk"]
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class AdminStockViewset(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = AdminStockSerializer

    def get_queryset(self):
        color_id = self.kwargs["color_pk"]
        return super().get_queryset().filter(color__id=color_id)
