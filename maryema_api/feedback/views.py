from rest_framework import viewsets

from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
