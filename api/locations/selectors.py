from django.db.models.query import QuerySet

from .models import City, Governorate


def list_governorate() -> QuerySet[Governorate]:
    return Governorate.objects.all()


def list_cities() -> QuerySet[City]:
    return City.objects.all()
