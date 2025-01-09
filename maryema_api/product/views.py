from profile.serializers import UserSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.permissions import IsAdmin
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
            return VariantSerializer
        return writeVariantSerializer

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="add-to-wishlist",
    )
    def add_to_wishlist(self, request, pk):
        variant = self.get_object()
        current_user_wishlist = request.user.profile.wishlist
        if variant in current_user_wishlist.all():
            return Response(
                {"error": f"{variant} is already in your wishlist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_user_wishlist.add(variant)
        return Response(
            {"details": f"{variant} is added to your whishlist successfuly"},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="remove-from-wishlist",
    )
    def remove_from_wishlist(self, request, pk):
        variant = self.get_object()
        current_user_wishlist = request.user.profile.wishlist
        if variant not in current_user_wishlist.all():
            return Response(
                {"error": f"{variant} is not in your wishlist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_user_wishlist.remove(variant)
        return Response(
            {"detail": f"{variant} is removed successfuly."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsAdmin],
        url_path="wished-by",
    )
    def wished_by(self, request, pk):
        variant = self.get_object()
        wished_by = variant.wished_by.select_related("user").all()
        wishing_users = [profile.user for profile in wished_by]

        paginator = PageNumberPagination()
        paginated_wishing_users = paginator.paginate_queryset(wishing_users, request)

        serializer = UserSerializer(
            paginated_wishing_users, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(serializer.data)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadCollectionSerializer
        return WriteCollectionSerializer
