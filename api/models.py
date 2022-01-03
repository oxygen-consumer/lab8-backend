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

    @property
    def workmanship_sum(self):
        transactions = Transaction.objects.all()
        ans = 0.0
        for transaction in transactions:
            if transaction.car == self:
                ans += transaction.paid_workmanship_price
        return ans

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

    @property
    def client_discount(self):
        transactions = Transaction.objects.all()
        ans = 0.0
        for transaction in transactions:
            if transaction.client == self:
                ans += transaction.workmanship_discount
        return ans

    def __str__(self) -> str:
        return str(self.id) + ": " + self.first_name + " " + self.last_name


class Transaction(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="transactions"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
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

    @property
    def parts_discount(self) -> float:
        if self.car.on_warranty:
            return float(self.parts_price)
        else:
            return 0.0

    @property
    def workmanship_discount(self) -> float:
        if self.client:
            return float(self.workmanship_price) * 0.1
        else:
            return 0.0

    @property
    def paid_parts_price(self) -> float:
        return float(self.parts_price) - self.parts_discount

    @property
    def paid_workmanship_price(self) -> float:
        return float(self.workmanship_price) - self.workmanship_discount

    @property
    def total_price(self) -> float:
        return self.paid_parts_price + self.paid_workmanship_price

    @property
    def total_discount(self) -> float:
        return self.workmanship_discount + self.parts_discount
