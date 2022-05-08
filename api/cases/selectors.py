from django.core.exceptions import PermissionDenied
from django.db.models.query import Q, QuerySet
from django.shortcuts import get_object_or_404

from api.users.models import User

from .filters import CaseFilter
from .models import Case, CaseMatch


def get_case(*, pk: int, fetched_by: User) -> Case:
    case = get_object_or_404(Case, pk=pk)

    if not (case.is_active or fetched_by == case.user):
        raise PermissionDenied()

    return case


def list_case(*, filters=None) -> QuerySet[Case]:
    filters = filters or {}

    # TODO Switch to posted cases only
    qs = Case.objects.filter(posted_at__isnull=False)

    return CaseFilter(filters, qs).qs


def list_user_case(*, user: User):
    return user.cases.all()


def list_case_match(*, pk: int, fetched_by: User) -> QuerySet[Case]:
    case = get_object_or_404(Case, pk=pk)

    if fetched_by != case.user:
        raise PermissionDenied()

    # TODO Wrong approach
    qs = CaseMatch.objects.filter(Q(case=case) | Q(match=case))
    return qs
