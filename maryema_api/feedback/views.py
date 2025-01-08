from rest_framework import permissions, viewsets

from core.permissions import IsOwner
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
