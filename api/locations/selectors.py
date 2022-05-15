from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from .models import City, Governorate


def list_governorate() -> QuerySet[Governorate]:
    return Governorate.objects.all()


def list_governorate_cities(gov_id) -> QuerySet[City]:
    gov = get_object_or_404(Governorate, pk=gov_id)
    return gov.cities.all()
