from typing import Optional

from ..locations.models import Location
from .models import User


def create_user(
    *,
    full_name: str,
    username: str,
    password: str,
    email: Optional[str] = None,
    firebase_token: Optional[str],
    location: Location
) -> User:

    user = User(
        full_name=full_name,
        username=username,
        email=email,
        firebase_token=firebase_token,
        location=location,
    )
    user.set_password(password)
    user.full_clean()
    user.save()

    return user
