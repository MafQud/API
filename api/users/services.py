from typing import Optional

from ..locations.models import Location
from .models import User


def create_user(
    *, full_name: str, username: str, email: Optional[str], location: Location
) -> User:

    user = User(full_name=full_name, username=username, email=email, location=location)
    user.full_clean()
    user.save()

    return user
