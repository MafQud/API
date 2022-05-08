from typing import Dict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

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
    firebase_token: str,
    location: Dict,
) -> User:

    # Creating user's related entities
    location: Location = create_location(**location)

    # Pack user data for validation
    user: User = User(
        name=name, username=username, firebase_token=firebase_token, location=location
    )

    # Password validation
    validate_password(password)
    user.password = make_password(password)

    # Data validation
    user.full_clean()

    # Saving user to the database
    user.save()

    return user


@transaction.atomic
def update_user(
    *,
    user: User,
    data: Dict,
) -> User:
    non_side_effect_fields = ["name", "firebase_token"]

    user, _ = model_update(
        instance=user,
        fields=non_side_effect_fields,
        data=data,
    )

    location_data = data.get("location")
    if location_data:
        update_location(location=user.location, data=location_data)

    return user
