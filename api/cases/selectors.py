from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
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


def list_case_match(*, case: Case, fetched_by: User) -> QuerySet[CaseMatch]:

    if case.user != fetched_by:
        raise PermissionDenied()

    qs = []

    if case.type == Case.Types.FOUND:
        qs = case.found_matches.all()

    elif case.type == Case.Types.MISSING:
        qs = case.missing_matches.all()

    return qs


def list_user_cases(user: User) -> QuerySet[Case]:
    return user.cases.all()
