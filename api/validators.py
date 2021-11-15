from django.core.exceptions import ValidationError
from datetime import date


def validate_year(value):
    if value > date.today().year:
        raise ValidationError(f"Nu suntem inca in anul {value}")


def validate_cnp(value):
    if len(str(value)) != 13:
        raise ValidationError("CNP-ul nu este valid")


def validate_date(value):
    if value > date.today():
        raise ValidationError("Nu suntem inca in aceasta data")


def validate_price(value):
    if isinstance(value, str) or value < 0:
        raise ValidationError("Pretul nu este corect")
