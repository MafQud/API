from django.core.exceptions import ValidationError


def is_phone(val: str):
    """
    Validates a phone number
    """
    if not val.isnumeric() or len(val) != 10:
        raise ValidationError(f'"Phone: {val}" is not a valid number')


def is_national_id(val: str):
    """
    Validates an egyptian national id
    """
    if not val.isnumeric() or len(val) != 14:
        raise ValidationError(f'"ID: {val}" is not a valid national id')
