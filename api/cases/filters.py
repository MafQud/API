import django_filters
from django.db.models.query import Q

from .models import Case


class CaseFilter(django_filters.FilterSet):

    type = django_filters.CharFilter(lookup_expr="iexact")

    gov = django_filters.NumberFilter(field_name="location__gov")
    name = django_filters.CharFilter(field_name="details__name", method="filter_name")

    start_age = django_filters.NumberFilter(
        field_name="details__age", lookup_expr="gte"
    )
    end_age = django_filters.NumberFilter(field_name="details__age", lookup_expr="lte")

    start_date = django_filters.DateFilter(
        field_name="details__last_seen", lookup_expr="gte"
    )
    end_date = django_filters.DateFilter(
        field_name="details__last_seen", lookup_expr="lte"
    )

    def filter_name(self, queryset, name, value):
        if self.data.get("include_null"):
            return queryset.filter(
                Q(details__name__icontains=value) | Q(details__name__isnull=True)
            )

        return queryset.filter(details__name__icontains=value)

    class Meta:
        model = Case
        fields = [
            "type",
            "details__age",
            "details__last_seen",
            "location__gov",
            "details__name",
        ]
