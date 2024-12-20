import uuid

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from feedbacks.serializers import FeedbackSerializer
from products.models import Category, Division, Product
from products.serializers import (
    AdminProductSerlaizer,
    CategoryListSerializer,
    CategorySerializer,
    DivisionSerializer,
    ProductDetailSerializer,
    ProductSerializer,
)
from stock.models import Color
from stock.serializers import FilterColorSerializer


class ProductViewSet(viewsets.GenericViewSet):
    queryset = Product.objects.all().order_by("-created_at")

    def list(self, request, *args, **kwargs):
        filter_params = {}
        division_id = request.query_params.get("division")
        category_id = request.query_params.get("category")

        # color = request.query_params.get("color")
        # size = request.query_params.get("size")
        # min_price = request.query_params.get("min_price")
        # max_price = request.query_params.get("max_price")

        if division_id:
            try:
                # Check if the division ID is a valid UUID
                uuid.UUID(division_id)

                # Check if the division exists
                if not Division.objects.filter(id=division_id).exists():
                    raise ValidationError({"division": "Division does not exist"})
                filter_params["category__division__id"] = division_id
            except ValueError:
                raise ValidationError({"division": "Invalid ID"})

        if category_id:
            try:
                # Check if the category ID is a valid UUID
                uuid.UUID(category_id)

                # Check if the category exists
                if not Category.objects.filter(id=category_id).exists():
                    raise ValidationError({"category": "Category does not exist"})

                # Check if the category exists within the selected division
                if division_id:
                    if not Category.objects.filter(
                        id=category_id, division__id=division_id
                    ).exists():
                        raise ValidationError(
                            {"category": "Category must exist in the selected division"}
                        )
                filter_params["category__id"] = category_id
            except ValueError:
                raise ValidationError({"category": "Invalid ID"})

        # Filter the queryset based on the provided params
        queryset = self.filter_queryset(self.get_queryset()).filter(**filter_params)

        # Paginate the queryset
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        feedbacks = instance.feedbacks.all().order_by("-rate")[:5]
        serialized_feedbacks = FeedbackSerializer(feedbacks, many=True)
        serializer = ProductDetailSerializer(instance)
        data = serializer.data
        data["feedbacks"] = serialized_feedbacks.data
        return Response(data)


class FeedbackViewSet(viewsets.GenericViewSet):
    """ViewSet for the Feedback model of a product"""

    def list(self, request, *args, **kwargs):
        product_id = request.params.get("product_id")

        product = Product.objects.get(id=product_id)
        feedbacks = product.feedbacks.all().order_by("-rate")

        page = self.paginate_queryset(feedbacks)

        if page is not None:
            serializer = FeedbackSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        product_id = request.params.get("product")
        product = Product.objects.get(id=product_id)
        data = request.data
        data["product"] = product.id

        serializer = FeedbackSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class FilterDataView(APIView):
    def get(self, request, *args, **kwargs):
        division_id = request.query_params.get("division")
        category_id = request.query_params.get("category")
        color_id = request.query_params.getlist("color")

        # filter the divisions based on the provided division_id or retrieve all
        if division_id:
            divisions = Division.objects.filter(id=division_id)
        else:
            divisions = Division.objects.all()

        # only return categories that belong to the selected division
        categories = Category.objects.filter(
            division__in=divisions,
        )

        # filter the rest of the categories based on the provided category_id or retrieve all
        if category_id:
            categories = categories.filter(id=category_id)

        # only return colors that belong to the selected categories
        colors = Color.objects.filter(product__category__in=categories)

        # filter the rest of the colors based on the provided color_id or retrieve all
        if color_id:
            colors = colors.filter(id__in=color_id)

        division_serializer = DivisionSerializer(divisions, many=True)
        category_serializer = CategorySerializer(categories, many=True)
        color_serializer = FilterColorSerializer(colors, many=True)

        return Response(
            {
                "divisions": division_serializer.data,
                "categories": category_serializer.data,
                "colors": color_serializer.data,
            }
        )

    # implement it just to pass the error
    # I have no idea what this method is supposed to do
    @classmethod
    def get_extra_actions(cls):
        return []


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class AdminProducViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AdminProductSerlaizer
