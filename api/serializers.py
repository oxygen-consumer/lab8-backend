from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Car, Client, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class CarSerializer(serializers.ModelSerializer):
    workmanship_sum = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True, default=0
    )

    class Meta:
        model = Car
        fields = [
            "id",
            "model",
            "acquisition_year",
            "kilometers",
            "on_warranty",
            "workmanship_sum",
        ]


class ClientSerializer(serializers.ModelSerializer):
    client_discount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True, default=0
    )

    class Meta:
        model = Client
        fields = [
            "id",
            "first_name",
            "last_name",
            "CNP",
            "birth_date",
            "join_date",
            "client_discount",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "id_car",
            "id_client",
            "parts_price",
            "workmanship_price",
            "time",
            "parts_discount",
            "workmanship_discount",
            "total_discount",
        ]
