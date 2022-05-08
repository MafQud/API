from typing import Dict, Optional

from django.db import transaction
from django.shortcuts import get_object_or_404

from api.common.services import model_update
from api.locations.models import Location
from api.locations.services import create_location, update_location
from api.users.models import User


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


@transaction.atomic
def update_user(
    *,
    user_id: int,
    data: Dict,
) -> User:
    fields = ["name", "email"]

    user = get_object_or_404(User, pk=user_id)

    gov_id = data.get("gov_id")
    city_id = data.get("city_id")

    if gov_id and city_id:
        update_location(
            location_id=user.location.id,
            data={
                "gov_id": data.get("gov_id"),
                "city_id": data.get("city_id"),
            },
        )

    user, _ = model_update(
        instance=user,
        fields=fields,
        data=data,
    )

    return user


def set_national_id(*, user_id: int, national_id: str) -> User:
    user = get_object_or_404(User, pk=user_id)
    user.national_id = national_id

    user.full_clean()
    user.save()

    return user
