from typing import Union

from django.core.exceptions import ValidationError


def is_national_id(val: str) -> Union[None, ValidationError]:
    if not val.isnumeric() or len(val) != 14:
        raise ValidationError(f"ID: {val} is not a valid egyptian national id")
