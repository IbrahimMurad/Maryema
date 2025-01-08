from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from feedback.serializers import FeedbackSerializer
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
from product.permissions import IsAdminOrReadOnly
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
    permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminOrReadOnly]


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminOrReadOnly]


class ImgViewSet(viewsets.ModelViewSet):
    queryset = Img.objects.all()
    serializer_class = ImgSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(
        methods=["GET", "POST"],
        detail=True,
        serializer_class=FeedbackSerializer,
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def feedback(self, request, pk):
        product = self.get_object()
        if request.method == "POST":
            serializer = FeedbackSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save(product=product)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        feedbacks = product.feedbacks.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)


class VariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return writeVariantSerializer
        return VariantSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadCollectionSerializer
        return WriteCollectionSerializer
