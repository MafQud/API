from typing import Dict, Optional

from django.db import transaction
from django.shortcuts import get_object_or_404

from api.common.services import model_update
from api.locations.models import Location
from api.locations.services import create_location
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
    fields = ["name", "email", "location"]

    user = get_object_or_404(User, pk=user_id)
    old_location = user.location

    location_updated = False
    city_id = data.get("city_id")

    if (city_id is not None) and (user.location.city.id != city_id):
        location = create_location(
            gov_id=data.get("gov_id"),
            city_id=data.get("city_id"),
        )
        data["location"] = location

        location_updated = True

    user, has_updated = model_update(
        instance=user,
        fields=fields,
        data=data,
    )

    # Clean old location
    if location_updated:
        old_location.delete()

    return user, has_updated
