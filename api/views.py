from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Car, Client, Transaction
from .serializers import (
    UserSerializer,
    CarSerializer,
    ClientSerializer,
    TransactionSerializer,
)
from django.contrib.auth.models import User
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().annotate(
        workmanship_price=Sum("transactions__workmanship_price")
    )
    serializer_class = CarSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "id",
        "model",
        "acquisition_year",
        "kilometers",
        "workmanship_price",
    ]
    ordering = ["-workmanship_price"]


class ClientViewSet(viewsets.ModelViewSet):
    # queryset = Client.objects.all().annotate(
    #     client_discount=Sum("transactions__workmanship_discount")
    # )
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "id",
        "first_name",
        "last_name",
        "CNP",
        "birth_date",
        "join_date",
        "client_discount",
    ]
    # ordering = ["-client_discount"]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["time"]
