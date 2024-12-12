import logging

from rest_framework import status, viewsets
from rest_framework.response import Response

from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer

logger = logging.getLogger(__name__)


class FeedbackViewSet(viewsets.ModelViewSet):
    """Viewset for the Feedback model"""

    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.filter(product_id=self.kwargs["product_pk"])

    def list(self, request, *args, **kwargs):
        feedbacks = self.get_queryset()
        serializer = self.get_serializer(feedbacks, many=True)
        data = serializer.data
        return Response(data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["customer"] = request.user.profile.id
        data["product"] = kwargs.get("product_pk")
        serializer = self.get_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.profile != instance.customer:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"detail": "You do not have permission to perform this action."},
            )
        data = request.data.copy()
        data["customer"] = request.user.profile.id
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.profile != instance.customer:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"detail": "You do not have permission to perform this action."},
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
