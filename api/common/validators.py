from typing import Union

from django.core.exceptions import ValidationError


def is_national_id(val: str) -> Union[None, ValidationError]:
    """
    Validates and egyptian national id
    """
    if not val.isnumeric() or len(val) != 14:
        raise ValidationError(f"ID: {val} is not a valid egyptian national id")


def is_phone(val: str):
    """
    Validates a phone number
    """
    if not val.isnumeric() or len(val) != 10:
        raise ValidationError(f'"{val}" is not a valid number')
