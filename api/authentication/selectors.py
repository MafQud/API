from typing import Union

from rest_framework.exceptions import ValidationError

from api.users.models import User


def validate_phone(*, phone: str) -> Union[None, ValidationError]:
    if User.objects.filter(username=phone).exists():
        raise ValidationError(f"Phone number: {phone} already taken")

    return None
