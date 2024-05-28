from django.shortcuts import render
from rest_framework import viewsets
from .models import MainAccountBalance, Profile
from .serializers import (
    AccountBalanceSerializer,
    ProfileSerializer,
    BonusBalanceSerializer,
    UserSerializer,
    TotalWinningsSerializer,
)
from .serializers import AccountBalanceSerializer, MainAccountBalance, TotalWinnings
from django.contrib.auth.models import User
from .permissions import IsAuthorOrAdmin, IsAdminOrReadOnly


# Create your views here.
class TotalWinningsViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = TotalWinnings.objects.select_related("user")
    serializer_class = TotalWinningsSerializer
    filterset_fields = ("user",)


class MainAccountBalanceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = MainAccountBalance.objects.select_related("user")
    filterset_fields = "user"
    serializer_class = AccountBalanceSerializer


class BonusAccountBalanceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = MainAccountBalance.objects.prefetch_related("user")
    filterset_fields = ("user",)
    serializer_class = BonusBalanceSerializer


class ProfileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrAdmin]
    queryset = Profile.objects.select_related(
        "user",
    )
    serializer_class = ProfileSerializer
    filterset_fields = ("email", "main_phone_number", "username")


class UserViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrAdmin]
    queryset = User.objects.select_related(
        "profile",
    )
    serializer_class = UserSerializer
    filterset_fields = "username"
