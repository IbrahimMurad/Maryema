from rest_framework import viewsets

from product.models import (
    Category,
    Collection,
    Color,
    Division,
    Img,
    Product,
    ProductVariant,
    Size,
)
from product.serializers import (
    CategorySerializer,
    ColorSerializer,
    DivisionSerializer,
    ImgSerializer,
    ProductSerializer,
    ReadCollectionSerializer,
    SizeSerializer,
    VariantSerializer,
    WriteCollectionSerializer,
    writeVariantSerializer,
)


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ImgViewSet(viewsets.ModelViewSet):
    queryset = Img.objects.all()
    serializer_class = ImgSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class VariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = VariantSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return writeVariantSerializer
        return VariantSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadCollectionSerializer
        return WriteCollectionSerializer
