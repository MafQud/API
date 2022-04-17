from typing import Iterable

from .models import City, Governorate


def list_governorate() -> Iterable[Governorate]:
    return Governorate.objects.all()


def list_cities() -> Iterable[City]:
    return City.objects.all()
