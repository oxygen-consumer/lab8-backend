from django.db import models
from datetime import date
from .validators import *


class Car(models.Model):
    model = models.CharField(max_length=100)
    acquisition_year = models.PositiveIntegerField(validators=[validate_year])
    kilometers = models.PositiveIntegerField()

    @property
    def on_warranty(self):
        if (
            date.today().year - self.acquisition_year <= 3
            and self.kilometers <= 60000
        ):
            return True
        else:
            return False

    def __str__(self):
        return str(self.id) + ": " + self.model


class Client(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    CNP = models.PositiveBigIntegerField(
        unique=True, validators=[validate_cnp]
    )
    birth_date = models.DateField(validators=[validate_date])
    join_date = models.DateField(auto_now_add=True, validators=[validate_date])

    def __str__(self) -> str:
        return str(self.id) + ": " + self.first_name + " " + self.last_name


class Transaction(models.Model):
    id_car = models.ForeignKey(
        Car, on_delete=models.PROTECT, related_name="transactions"
    )
    id_client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="transactions",
    )
    workmanship_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_price]
    )
    parts_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_price]
    )
    time = models.DateTimeField(auto_now_add=True)
    workmanship_discount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_price]
    )
    parts_discount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_price]
    )

    @property
    def total_discount(self):
        return "{:.2f}".format(self.discount_parts + self.discount_workmanship)
