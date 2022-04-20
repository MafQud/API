from typing import Optional

from django.db import transaction

from ..locations.models import Location
from ..locations.services import create_location
from .models import User


@transaction.atomic
def create_user(
    *,
    name: str,
    username: str,
    password: str,
    email: Optional[str] = None,
    firebase_token: Optional[str],
    gov_id: int,
    city_id: int,
) -> User:

    loc: Location = create_location(gov_id=gov_id, city_id=city_id)
    user: User = User(
        name=name,
        username=username,
        email=email,
        location=loc,
        firebase_token=firebase_token,
    )
    user.set_password(password)
    user.full_clean()
    # user.clean()
    user.save()

    return user
