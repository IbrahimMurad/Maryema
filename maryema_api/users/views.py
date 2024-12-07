from django.contrib.auth.models import User
from rest_framework import viewsets

from users.serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(profile__role="customer")
    serializer_class = UserSerializer
