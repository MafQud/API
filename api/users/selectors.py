from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from api.cases.models import Case
from api.users.models import User


def get_user(user_id: int) -> User:
    return get_object_or_404(User, pk=user_id)


def get_user_cases(user: User) -> QuerySet[Case]:
    return user.cases.all()
