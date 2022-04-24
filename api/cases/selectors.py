from django.core.exceptions import PermissionDenied

from api.common.utils import get_object
from api.users.models import User

from .models import Case


def get_case(*, pk: int, fetched_by: User) -> Case:
    case = get_object(Case, pk=pk)
    if case.is_active or fetched_by == case.user:
        return case

    raise PermissionDenied()
