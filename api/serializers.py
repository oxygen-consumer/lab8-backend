from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Car, Client, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class CarSerializer(serializers.ModelSerializer):
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
            "car",
            "client",
            "time",
            "parts_price",
            "workmanship_price",
            "paid_parts_price",
            "paid_workmanship_price",
            "total_price",
            "total_discount",
            "parts_discount",
            "workmanship_discount",
        ]
