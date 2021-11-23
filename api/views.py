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
from rest_framework.response import Response
# from random import random, randrange
import random
from rest_framework.decorators import action
from .car_brands import car_brands


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

    @action(detail=False, methods=["get", "post"])
    def generateRandom(self, request):
        generated = []
        for x in range(int(request.data["num"])):
            obj = {
                "model": random.choice(car_brands),
                "acquisition_year": random.randrange(1950, 2021),
                "kilometers": random.randrange(600000),
            }
            generated.append(obj)
            Car.objects.create(
                model=obj["model"],
                acquisition_year=obj["acquisition_year"],
                kilometers=obj["kilometers"]
            )
        return Response(generated)


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
