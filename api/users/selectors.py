from django.shortcuts import get_object_or_404

from api.users.models import User


def get_user(user_id: int) -> User:
    return get_object_or_404(User, pk=user_id)
