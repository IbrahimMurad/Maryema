"""
This module contains the viewsets for the product app
"""

from profile.serializers import UserSerializer

from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.permissions import IsAdmin
from feedback.serializers import FeedbackSerializer
from product.filters import ProductFilter
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
    ProductDetailPublicSerializer,
    ProductListPublicSerializer,
    ProductSerializer,
    ReadCollectionSerializer,
    SizeSerializer,
    VariantSerializer,
    WriteCollectionSerializer,
    WriteVariantSerializer,
)


class DivisionViewSet(viewsets.ModelViewSet):
    """
    A viewset for the Division model

    It allows all users to read the divisions but only admin users can create, update or delete them
    """

    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for the Category model

    It allows all users to read the categories but only admin users can create, update or delete them
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ColorViewSet(viewsets.ModelViewSet):
    """
    A viewset for the Color model

    It allows all users to read the colors but only admin users can create, update or delete them
    """

    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminOrReadOnly]


class SizeViewSet(viewsets.ModelViewSet):
    """
    A viewset for the Size model

    It allows all users to read the sizes but only admin users can create, update or delete them
    """

    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminOrReadOnly]


class ImgViewSet(viewsets.ModelViewSet):
    """
    A viewset for the Img model

    It allows all users to read the images but only admin users can create, update or delete them
    """

    queryset = Img.objects.all()
    serializer_class = ImgSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for the Product model that provides the following <b>extra</b> actions:

    - `feedback`: Get or add feedbacks for a product

    It also, provides different serializers based on user type and action
    """

    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "name",
        "tags",
        "collection__name",
    ]
    ordering_fields = ["created_at", "variant__price"]
    filterset_class = ProductFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.profile.is_admin:
            return Product.objects.all()
        return Product.objects.filter(variant__isnull=False)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and user.profile.is_admin:
            return ProductSerializer
        if self.action == "list":
            return ProductListPublicSerializer
        return ProductDetailPublicSerializer

    @action(
        methods=["GET", "POST"],
        detail=True,
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def feedback(self, request, pk):
        product = self.get_object()
        if request.method == "POST":
            serializer = FeedbackSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                try:
                    serializer.save(product=product)
                    return Response(serializer.data)
                except ValidationError as e:
                    return Response(
                        {"error": e.messages},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(serializer.errors, status=400)
        feedbacks = product.feedbacks.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)


class VariantViewSet(viewsets.ModelViewSet):
    """A viewset for the ProductVariant model that provides the following extra actions:

    - `add_to_wishlist`: Add the variant to the current user's wishlist

    - `remove_from_wishlist`: Remove the variant from the current user's wishlist

    - `wished_by`: Get the users who have added this variant to their wishlist

    All users can read the variants but only authenticated users can add or remove them from their wishlist.

    Also, only admin users can create, update or delete them.
    """

    queryset = ProductVariant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return VariantSerializer
        return WriteVariantSerializer

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="add-to-wishlist",
    )
    def add_to_wishlist(self, request, pk):
        """Add this variant to the current user's wishlist"""

        variant = self.get_object()
        current_user_wishlist = request.user.profile.wishlist
        if variant in current_user_wishlist.all():
            return Response(
                {"error": f"{variant} is already in your wishlist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_user_wishlist.add(variant)
        return Response(
            {"detail": f"{variant} is added to your wishlist successfully"},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="remove-from-wishlist",
    )
    def remove_from_wishlist(self, request, pk):
        """Remove this variant from the current user's wishlist"""
        variant = self.get_object()
        current_user_wishlist = request.user.profile.wishlist
        if variant not in current_user_wishlist.all():
            return Response(
                {"error": f"{variant} is not in your wishlist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_user_wishlist.remove(variant)
        return Response(
            {"detail": f"{variant} is removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsAdmin],
        url_path="wished-by",
    )
    def wished_by(self, request, pk):
        """Get the users who have added this variant to their wishlist"""
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
    """
    A viewset for the Collection model

    Only admin user can perform write actions on this model.

    Different schemas are used for read and write actions.
    """

    queryset = Collection.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadCollectionSerializer
        return WriteCollectionSerializer
