from rest_framework import status, viewsets
from rest_framework.response import Response

from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    """Viewset for the Feedback model"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def create(self, request, *args, **kwargs):
        request.data["customer"] = request.user.profile.id
        serializer = self.get_serializer(data=request.data)
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
        request.data["customer"] = request.user.profile.id
        serializer = self.get_serializer(instance, data=request.data)
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
